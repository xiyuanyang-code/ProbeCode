import os
import sys
import asyncio
import nest_asyncio
from typing import List, Dict, Union

sys.path.append(os.getcwd())


from anthropic import Anthropic, APIStatusError
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from CodingAgent.llm.agent.base_chat import BaseChat
from CodingAgent.llm.agent.memory import MemoryManager


nest_asyncio.apply()


class MCPChat(BaseChat):
    """
    A chat implementation that uses the Anthropic LLM and connects to an
    external tool server via the MCP (Multi-Client Protocol) protocol.

    This class orchestrates the entire chat flow, managing the connection
    to an external tool server, interacting with the LLM (Large Language Model),
    and utilizing a MemoryManager to handle conversation context.
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Initializes the chat client, LLM client, and memory manager.

        Args:
            config_file (str): The path to the configuration file.
        """
        super().__init__(config_file)
        self.model_list = self.config.get("model", {}).get("model_name", [])
        self.session: ClientSession = None
        self.exit_stack = AsyncExitStack()

        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")

        self.llm_client = Anthropic(
            api_key=anthropic_api_key,
            base_url=os.environ.get("ANTHROPIC_BASE_URL"),
        )

        # Instantiate the MemoryManager to handle conversation history
        self.memory_manager = MemoryManager(self.config, self.llm_client)

    def _simple_chat(self, messages: List[Dict]) -> Dict:
        """
        Communicates with the LLM by sending a list of messages.

        This method attempts to get a response from the LLM using the models
        specified in the configuration, trying each model in the list sequentially
        in case of an API failure.

        Args:
            messages (List[Dict]): The list of message dictionaries representing
                                   the conversation history and the current prompt.

        Returns:
            Dict: The LLM's response object.

        Raises:
            RuntimeError: If all configured models fail to provide a response.
        """
        for i, model in enumerate(self.model_list):
            try:
                response = self.llm_client.messages.create(
                    max_tokens=2024,
                    model=model,
                    tools=self.available_tools,
                    messages=messages,
                )
                return response
            except APIStatusError as e:
                self.logger.warning(f"Model '{model}' failed. Error: {e.response.text}")
                if i < len(self.model_list) - 1:
                    next_model = self.model_list[i + 1]
                    self.logger.warning(f"Attempting with the next model: {next_model}")
                    continue
                else:
                    self.logger.error("All models failed. No more models to try.")
                    raise RuntimeError("All models failed.") from e

    async def connect(self, server_name: str):
        """
        Establishes a connection to the external tool server via MCP.

        This method initializes the client session, lists the available tools
        from the server, and starts the main chat loop.

        Args:
            server_name (str): The name of the server to connect to, as defined
                               in the configuration file.

        Raises:
            ValueError: If the server configuration is not found.
            Exception: If the connection to the server fails.
        """
        server_configs = self.config.get("servers", {})
        server_config = server_configs.get(server_name)
        if not server_config:
            raise ValueError(f"Server configuration for '{server_name}' not found.")

        server_env = os.environ.copy()
        server_env.update(server_config.get("env", {}))

        server_params = StdioServerParameters(
            command=server_config.get("command"),
            args=server_config.get("args"),
            env=server_env,
        )

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    await session.initialize()

                    response = await session.list_tools()
                    self.available_tools = [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema,
                        }
                        for tool in response.tools
                    ]
                    self.logger.notice(
                        f"Connected to server with tools: {[tool.name for tool in response.tools]}"
                    )

                    # resource config
                    response = await session.list_resource_templates()
                    self.available_resources = [
                        {
                            "name": resource.name,
                            "description": resource.description,
                            "uriTemplate": resource.uriTemplate
                        }
                        for resource in response.resourceTemplates
                    ]
                    self.logger.notice(
                        f"Connected to server with resources: {[resource.name for resource in response.resourceTemplates]}"
                    )


                    self.chat_loop()
        except Exception as e:
            self.logger.error(f"Failed to connect to the server: {e}")
            raise

    async def _process_query(self, query: str):
        """
        Processes a user query, manages the conversation flow, and interacts with tools.

        This is the main asynchronous loop for handling a single user turn.
        It checks for special commands (like '/memory'), updates the memory
        with the user's message, interacts with the LLM, and handles any
        tool use and tool results.

        Args:
            query (str): The user's input string.
        """
        # Check for special commands
        if query.strip().lower() == "/memory":
            self.logger.notice(
                "Received /memory command. Storing short-term memory into long-term memory..."
            )
            self.memory_manager.store_short_term_memory()
            self.user_chat.display_output(
                "✅ The current conversation has been successfully stored to long-term memory and will not be compressed."
            )
            # Do not proceed with LLM call; wait for the next user input
            return

        # Add the new user message to the memory
        self.memory_manager.add_message({"role": "user", "content": query})

        # Get the full conversation context from the memory manager
        full_context = self.memory_manager.get_full_context()

        try:
            response = self._simple_chat(messages=full_context)
        except RuntimeError as e:
            self.logger.error(f"Chat failed to start: {e}")
            return

        while True:
            tool_use_content = next(
                (c for c in response.content if c.type == "tool_use"), None
            )

            if tool_use_content:
                tool_id = tool_use_content.id
                tool_args = tool_use_content.input
                tool_name = tool_use_content.name

                self.memory_manager.add_message(
                    {"role": "assistant", "content": [tool_use_content]}
                )
                self.logger.info(f"Calling tool '{tool_name}' with args: {tool_args}")

                if not self.session:
                    self.logger.error("MCP session is not established.")
                    return

                try:
                    result = await self.session.call_tool(
                        tool_name, arguments=tool_args
                    )
                    tool_result_content: Union[str, Dict]
                    if isinstance(result.content, (str, dict, list)):
                        tool_result_content = result.content
                    else:
                        tool_result_content = repr(result.content)

                except Exception as e:
                    self.logger.error(f"Error calling tool '{tool_name}': {e}")
                    tool_result_content = {"error": str(e)}

                tool_result_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": tool_result_content,
                        }
                    ],
                }
                self.memory_manager.add_message(tool_result_message)

                # Get the updated context, which now includes the tool result, and send to LLM
                response = self._simple_chat(
                    messages=self.memory_manager.get_full_context()
                )

            else:
                # The LLM has provided a final text response
                for content in response.content:
                    if content.type == "text":
                        final_message = {"role": "assistant", "content": content.text}
                        self.memory_manager.add_message(final_message)
                        self.user_chat.display_output(content.text)
                break

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


# for testing only
async def main():
    """
    Main function to initialize and run the chatbot.
    """
    try:
        chatbot = MCPChat(config_file="./MCPChatBot/config.json")
        await chatbot.connect(server_name="tools")
    except Exception as e:
        print(f"Failed to run the chatbot: {e}")


if __name__ == "__main__":
    asyncio.run(main())
