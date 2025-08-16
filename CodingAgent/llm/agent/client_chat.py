# mcp_chat.py
import os
import sys
import asyncio
import nest_asyncio
from typing import List, Dict

sys.path.append(os.getcwd())


from anthropic import Anthropic, APIStatusError
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from CodingAgent.llm.agent.base_chat import BaseChat


nest_asyncio.apply()


class MCPChat(BaseChat):
    """
    A chat implementation that uses the Anthropic LLM and connects to an
    external tool server via the MCP (Multi-Client Protocol) protocol.
    """

    def __init__(self, config_file: str = "config.json"):
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
                    self.chat_loop()
        except Exception as e:
            self.logger.error(f"Failed to connect to the server: {e}")
            raise

    async def _process_query(self, query: str):
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
                        self.user_chat.display_output(content.text)
                break


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
