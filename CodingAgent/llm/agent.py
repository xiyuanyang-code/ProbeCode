import os
import asyncio
import nest_asyncio
import json

from anthropic import Anthropic, APIStatusError
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import List, Dict
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


from CodingAgent.utils.log import setup_logging_config

# Apply nest_asyncio for compatibility in environments like Jupyter
nest_asyncio.apply()


class BaseChat:
    """
    A base class for implementing a multi-turn chat with a Large Language Model (LLM).

    This class provides the core structure for handling a chat loop, managing
    messages, and loading configurations. Subclasses must implement specific
    LLM logic and tool integration.
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Initializes the BaseChat instance.

        Args:
            config_file (str): The path to the configuration JSON file.
        """
        self.logger = setup_logging_config()
        self.config: Dict = self._load_config(config_file)
        self.llm_client = None
        self.available_tools: List[Dict] = []

    def _load_config(self, file_path: str) -> Dict:
        """
        Loads server configurations from a JSON file.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            Dict: The loaded configuration dictionary, or an empty dictionary if
                  loading fails.
        """
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from '{file_path}' successfully.")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file '{file_path}' not found.")
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(
                f"Failed to parse configuration from '{file_path}'. Details: {e}"
            )
        return {}

    async def _process_query(self, query: str):
        """
        Processes a single user query.

        This method must be overridden by subclasses to implement specific LLM
        interaction and tool-use logic.

        Args:
            query (str): The user's input query string.
        """
        raise NotImplementedError(
            "Subclasses must implement the _process_query method."
        )

    async def get_user_input(self):
        try:
            user_input = prompt(
                "Input your message: ",
                # history=self.history,
                auto_suggest=AutoSuggestFromHistory(),
            )
            return user_input.strip()
        except KeyboardInterrupt as e:
            self.logger.warning(f"EXITING MANUALLY: {e}")
            return "/exit"

    async def chat_loop(self):
        """
        Runs an interactive chat loop, prompting the user for input and
        processing queries until the user types 'quit'.
        """
        self.logger.notice("\nChatbot Started!")
        self.logger.notice("Type your queries or 'quit' to exit.")
        while True:
            try:
                query = await self.get_user_input()
                if query.lower() == "/quit" or query.lower() == "/exit":
                    self.logger.notice("Exiting chat loop.")
                    break
                await self._process_query(query)
            except Exception as e:
                self.logger.error(f"An error occurred during chat loop: {str(e)}")


class MCPChat(BaseChat):
    """
    A chat implementation that uses the Anthropic LLM and connects to an
    external tool server via the MCP (Multi-Client Protocol) protocol.

    This class handles LLM interactions, tool calls, and managing the
    conversation state with the tool server.
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Initializes the MCPChat instance, setting up the Anthropic client
        and loading the model configuration.

        Args:
            config_file (str): The path to the configuration JSON file.
        """
        super().__init__(config_file)
        self.model_list = self.config.get("model", {}).get("model_name", [])
        self.session: ClientSession = None

        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")

        self.llm_client = Anthropic(
            api_key=anthropic_api_key,
            base_url=os.environ.get("ANTHROPIC_BASE_URL"),
        )

    def _simple_chat(self, messages: List[Dict]) -> Dict:
        """
        Sends a list of messages to the Anthropic LLM, trying multiple models
        if the primary one fails.

        Args:
            messages (List[Dict]): The list of messages to send to the LLM.

        Returns:
            Dict: The response object from the LLM.

        Raises:
            RuntimeError: If all models fail to return a valid response.
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
        Connects to a single specified tool server and initiates the chat loop.

        Args:
            server_name (str): The name of the server to connect to, as defined
                               in the configuration file.
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
                    await self.chat_loop()
        except Exception as e:
            self.logger.error(f"Failed to connect to the server: {e}")
            raise

    async def _process_query(self, query: str):
        """
        Processes a single user query by interacting with the Anthropic LLM
        and executing tool calls via the MCP session.
        """
        messages = [{"role": "user", "content": query}]

        try:
            response = self._simple_chat(messages=messages)
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

                messages.append({"role": "assistant", "content": [tool_use_content]})
                self.logger.info(f"Calling tool '{tool_name}' with args: {tool_args}")

                if not self.session:
                    self.logger.error("MCP session is not established.")
                    return

                try:
                    result = await self.session.call_tool(
                        tool_name, arguments=tool_args
                    )
                    tool_result_content = result.content
                except Exception as e:
                    self.logger.error(f"Error calling tool '{tool_name}': {e}")
                    tool_result_content = {"error": str(e)}

                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": tool_result_content,
                            }
                        ],
                    }
                )
                response = self._simple_chat(messages=messages)

            else:
                for content in response.content:
                    if content.type == "text":
                        print(content.text)
                break


async def main():
    """
    Main function to initialize and run the chatbot.

    This function sets up the MCPChat instance and attempts to connect
    to a predefined server.
    """
    try:
        # Example of how to connect to a specific server.
        # Ensure 'config.json' and the server configuration are set up.
        chatbot = MCPChat(config_file="./MCPChatBot/config.json")
        await chatbot.connect(server_name="tools")
    except Exception as e:
        chatbot.logger.error(f"Failed to run the chatbot: {e}")


if __name__ == "__main__":
    asyncio.run(main())
