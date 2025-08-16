# LLM Component: MCPChatBot

## Introduction

The LLM module provides the core functionality for interacting with large language models in the CodingAgent project. It implements a chat interface that connects to external tools via the MCP (Multi-Client Protocol) and manages conversation context through a two-tiered memory system.

## Structure

The module is organized into several key components:

- `agent/`: Contains the core chat implementation
  - `base_chat.py`: Defines the base chat class with user interface handling
  - `client_chat.py`: Implements the MCP-based chat client with LLM integration
  - `memory.py`: Manages conversation context with short-term and long-term memory

- `tools/`: Houses tool implementations that can be used by the LLM
  - `file_ops.py`: File system operations (create, delete, move, etc.)
  - `web_search.py`: Web search functionality

- `mcp_tool_integrate.py`: Dynamically registers tools with the MCP server

- `config.json`: Configuration file for models and server settings

- `prompt.py`: Basic prompts for the coding agent

- `utils.py`: Utility functions for API key management

## Key Features

1. **MCP Integration**: Connects to external tool servers using the Multi-Client Protocol, allowing the LLM to access various tools.

2. **Memory Management**: Implements a two-tiered memory system:
   - Short-term memory: Stores recent conversation turns for immediate context
   - Long-term memory: Maintains compressed summaries of past conversations
   - Automatic summarization when short-term memory reaches a threshold
   - Manual storage of important context via the `/memory` command

3. **Model Fallback**: Supports multiple LLM models with automatic fallback if one model fails.

4. **Persistent History**: Automatically saves conversation history to timestamped files.

5. **Tool Integration**: Dynamically loads and registers tools that can be called by the LLM during conversations.

## Usage

The main entry point is the `MCPChat` class in `client_chat.py`. It requires a configuration file specifying the models to use and the tool server to connect to. The chat loop handles user input, LLM interaction, and tool calling automatically.

### Configs

> [!TIP]
> To be optimized

- For simple LLM response, we use `Anthropic` for our base model usage, thus `ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` are required.

    - Model Type and MCP config can be manually defined in [`config.json`](../llm/config.json)

    ```json
    {
        "model": {
            "model_name": [
                "claude-3-5-haiku-20241022",
                "claude-sonnet-4-20250514",
                // you can add more here...
                // the default calling sequence is by index.
            ]
        },
        "servers": {
            "tools": {
                "command": "uv",
                "args": [
                    "run",
                    "CodingAgent/llm/mcp_tool_integrate.py"
                ]
            }
        }
    }
    ```

    - If you want to customize your own MCP-tools, write functions and pretty docstring in `./CodingAgent/llm/tools` folder, and MCP server will automatically grasp all the functions and view them as available tools.
    - For Current supported tools, see [this docs](./CodingAgent/llm/tools/README.md).

- For web-search tools, `ZHIPU_API_KEY` is required in environment variables. We recommend you to write into your `~/.zshrc` or `~/.bashrc` file.

```bash
export ANTHROPIC_API_KEY="switch to yours"

# I just recommend this base url
export ANTHROPIC_BASE_URL="https://api.openai-proxy.org/anthropic"

# go to https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys to generating your own api-key!
export ZHIPU_API_KEY="switch to yours"
```

### Demo

![A simple Demo](https://github.com/xiyuanyang-code/Repo-Coding-Agent/blob/master/assets/imgs/ui_initial.png)