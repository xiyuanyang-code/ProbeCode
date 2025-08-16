# Repo-Coding Agent

> [!WARNING]
> This repo is still in construction process

> [!TIP]
> Congratulations! The initial dev release `0.1.1` are available! See [Usage](#release) for more detail.

## Introduction

We aim to create a **Repo Coding Agent** specializing in understanding extremely long and complex code blocks (even those exceeding the context length of an LLM). This agent will effectively read the relevant specialized code sections, thereby enhancing the LLM's code comprehension and generation capabilities for the given problem.

> [!TIP]
> It is just a toy implementation...
> Update: This project uses `uv` to manage environments.

## Current Constructing

Stage I: We want to let LLM accept the full content for all lines of code of the repository, which can better improve the comprehension of overall code for LLM. ✅

Stage II: Refactor the code & add basic code splitting tools. ✅

Stage III: Integrating more MCP configs and MCP tools for code splitting

- Optimize pyparser and inspector for MCP tools

- build final coding agent pipeline

- Add more MCP configs, including MCP prompt, resources and sampling.

Maybe in the next stage:

- Add frontend components (HTML & CSS & JavaScripts)

### Todo List

- [x] Complete the most basic functional design. ✅
- [x] Complete basic file matching, filtering and walking class and util functions. ✅
- [x] Complete the refactoring for the repo code structure for making it available as a python package. ✅
- [x] Complete the basic context management for stage one. ✅
- [x] Complete the model response. ✅
- [x] Couple the two modules and build the final pipeline. ✅
- [x] !REFACTOR: Remove camel. ✅
- [x] !REBUILD: Developing a simple and lightweight LLM multi-turn conversation mini-app with history management. ✅
    - [x] Complete basic model history management ✅
    - [x] Figure out how mainstream LLMs manage history records ✅
    - [x] Add advanced history settings. ✅
- [ ] Module: basic code splitting part constructing
    - [x] Add basic python parser using `ast`. ✅
    - [ ] Debug and add more functions for analyzing the tools
    - [ ] Integrate this independent modules into pipeline
    - [ ] View this as a MCP tool calling and refactor the code again
- [ ] MCP configuration
    - [x] Finish MCP tools settings
    - [ ] Restrict when LLM are enabled to call tools (optimize docstring)
    - [ ] Finish MCP prompts settings
    - [ ] Finish MCP resources settings
    - [ ] Finish MCP Sampling
    - Relevant Web: [MCP Components](https://huggingface.co/learn/mcp-course/en/unit1/key-concepts)

- [x] Fix: relative file path and using pip to install ✅
    - [x] Make the package can be run in any folder ✅
    - [x] Make the package can be installed with `pip install -e .` ✅
    - [x] Fix the problem for relative file path ✅




## Structure

```bash
.
├── CodingAgent
│   ├── __init__.py
│   ├── config.py
│   ├── config.yaml
│   ├── inspector
│   │   ├── __init__.py
│   │   └── context_manager.py
│   ├── llm
│   │   ├── __init__.py
│   │   ├── agent
│   │   │   ├── base_chat.py
│   │   │   ├── client_chat.py
│   │   │   └── memory.py
│   │   ├── config.json
│   │   ├── mcp_tool_integrate.py
│   │   ├── prompt.py
│   │   ├── tools
│   │   │   ├── file_ops.py
│   │   │   └── web_search.py
│   │   └── utils.py
│   ├── main.py
│   ├── pyparser
│   │   ├── README.md
│   │   ├── example
│   │   │   └── example.py
│   │   ├── parser.py
│   │   ├── result
│   │   │   └── test.json
│   │   └── test
│   │       ├── test_backward_compatibility.py
│   │       └── test_programmatic.py
│   └── utils
│       ├── __init__.py
│       └── logging_info.py
├── CodingAgent.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── requires.txt
│   └── top_level.txt
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── run.sh
└── uv.lock
```

## RELEASE

We are happy to announce that the initial light version of the CodingAgent `0.1.1` is available!
The current light version (dev) supports a lightweight command-line chat interface with history management and tool calls.

### Installation & Settings

#### Installation

Install several packages with `uv` or `pip`.

```bash
# python >= 3.10
git clone https://github.com/xiyuanyang-code/Repo-Coding-Agent.git
cd Repo-Coding-Agent

# install packages
# METHOD1: using uv (recommended)
bash scripts/run_with_uv.sh

# METHOD2: using pip
bash scripts/run.sh
```

#### Model Config Settings

To use the LLM module, see [Settings Tutorial](./CodingAgent/llm/README.md) for more information.

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
                    "/home/user/CodingAgent/llm/mcp_tool_integrate.py"
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

### Usage

The chat interface supports:
- Multi-turn conversations with context management
- Tool calling via MCP protocol (now supporting file operations and web search for Chinese and English)
- Agent Memory Management
    - Automatic memory compression for long conversations
    - Manual memory storage with the `/memory` command
    - Write history into local files.
- A beautiful CLI UI design.

```bash
# change to your current working directory
coding_agent

# then it will create a file named .history.txt which stores all the historical command you have typed in
# it will record the dialogue history in 'history' in the original folder (where you clone this project)
# logs will be saved here as well (in log in the original folder)
```

After typing the commands above, you can chat with the chatbox! Then it will create a file named `.history.txt` which stores all the historical command you have typed in. It will record the dialogue history in 'history' in the original folder (where you clone this project). Logs will be saved here as well (in log in the original folder)

### DEMO

Now the UI shows like that:

![A simple Demo](https://github.com/xiyuanyang-code/Repo-Coding-Agent/blob/master/assets/imgs/ui_initial.png)


## Contributions

All PRs are welcome. Email the author or raise an issue to communicate how to collaborate in this project.