import os
import asyncio
import nest_asyncio
import json

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import List, Dict

# Apply nest_asyncio for compatibility in environments like Jupyter
nest_asyncio.apply()


class BaseChat:
    """
    A base class for implementing a multi-turn chat with an LLM.
    Handles the core chat loop, query processing, and configuration loading.
    """

    def __init__(self, config_file: str = "config.json"):
        self.config: Dict = self._load_config(config_file)
        # LLM client and available tools are placeholders to be implemented in subclasses
        self.llm_client = None
        self.available_tools: List[Dict] = []

    def _load_config(self, file_path: str) -> Dict:
        """Loads server configurations from a JSON file."""
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            print(f"Configuration loaded from '{file_path}' successfully.")
            return config
        except FileNotFoundError:
            print(f"Error: Configuration file '{file_path}' not found.")
            return {}
        except (json.JSONDecodeError, KeyError) as e:
            print(
                f"Error: Failed to parse configuration from '{file_path}'. Details: {e}"
            )
            return {}

    async def _process_query(self, query: str):
        """
        Processes a single user query.
        This method should be overridden by subclasses to implement specific LLM logic.
        """
        raise NotImplementedError(
            "Subclasses must implement the _process_query method."
        )

    async def chat_loop(self):
        """Runs an interactive chat loop."""
        print("\nChatbot Started!")
        print("Type your queries or 'quit' to exit.")
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                await self._process_query(query)
                print("\n")
            except Exception as e:
                print(f"\nError: {str(e)}")


class MCPChat(BaseChat):
    """
    A specific chat implementation that uses the MCP protocol to connect to
    a server and use its tools with an Anthropic LLM.
    """

    def __init__(self, config_file: str = "config.json"):
        super().__init__(config_file)
        self.session: ClientSession = None
        self.llm_client = Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            base_url=os.environ.get("ANTHROPIC_BASE_URL"),
        )
        if not self.llm_client.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")

    async def connect_to_server_and_run(self, server_name: str):
        """Connects to a single specified server and runs the chat loop."""
        server_configs = self.config.get("servers", {})
        server_config = server_configs.get(server_name)
        if not server_config:
            raise ValueError(f"Server configuration for '{server_name}' not found.")

        # ! get env file
        server_env = os.environ.copy()
        server_env.update(server_config.get("env", {}))

        # ! you need to add this manually for functions and tools which will use environment variables
        if "ZHIPU_API_KEY" in os.environ:
            server_env["ZHIPU_API_KEY"] = os.environ["ZHIPU_API_KEY"]

        server_params = StdioServerParameters(
            command=server_config.get("command"),
            args=server_config.get("args"),
            # pass several local variables
            env=server_env,
        )

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

                print(self.available_tools)
                print(
                    f"\nConnected to server with tools: {[tool.name for tool in response.tools]}"
                )
                await self.chat_loop()

    async def _process_query(self, query: str):
        """Processes a single user query using the Anthropic LLM and MCP tools."""
        messages = [{"role": "user", "content": query}]

        # Initial call to the LLM
        response = self.llm_client.messages.create(
            max_tokens=2024,
            model="claude-3-7-sonnet-20250219",
            tools=self.available_tools,
            messages=messages,
        )

        while True:
            assistant_content = []
            for content in response.content:
                if content.type == "text":
                    print(content.text)
                    assistant_content.append(content)
                elif content.type == "tool_use":
                    assistant_content.append(content)
                    messages.append({"role": "assistant", "content": assistant_content})

                    tool_id = content.id
                    tool_args = content.input
                    tool_name = content.name
                    print(f"Calling tool {tool_name} with args {tool_args}")

                    if self.session is None:
                        raise RuntimeError("MCP session is not established.")

                    result = await self.session.call_tool(
                        tool_name, arguments=tool_args
                    )

                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": result.content,
                                }
                            ],
                        }
                    )
                    # Make a subsequent call to the LLM with the tool result
                    response = self.llm_client.messages.create(
                        max_tokens=2024,
                        model="claude-3-7-sonnet-20250219",
                        tools=self.available_tools,
                        messages=messages,
                    )
                    # Continue the loop to process the new response
                    break
            else:
                # If the loop finishes without a 'break', it means no tool was called,
                # and the response is complete.
                break


async def main():
    """Main function to initialize and run the chatbot."""
    try:
        # Example of how you would connect to a specific server.
        # You need to have a config.json with a server defined.
        chatbot = MCPChat(config_file="./MCPChatBot/config.json")
        await chatbot.connect_to_server_and_run(server_name="tools")
    except Exception as e:
        print(f"Failed to run the chatbot: {e}")


if __name__ == "__main__":
    asyncio.run(main())
