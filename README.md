# Repo-Coding Agent

> [!WARNING]
> This repo is still in construction process
> To be refactored

## Introduction

We aim to create a **Repo Coding Agent** specializing in understanding extremely long and complex code blocks (even those exceeding the context length of an LLM). This agent will effectively read the relevant specialized code sections, thereby enhancing the LLM's code comprehension and generation capabilities for the given problem.

> It is just a toy implementation...

>[!TIP]
>Update: This project uses `uv` to manage environments.

## Current Constructing

Stage I: We want to let LLM accept the full content for all lines of code of the repository, which can better improve the comprehension of overall code for LLM. ✅

> [!WARNING]
> We will not use `camel.agent.ChatAgent` as the fundamental agent, for it is too heavy.
> Thus the code needs to be refactored.

We need to implement:

- Show full context for large-language models.

- Add history management for multi LLM response.

- Finish the basic running pipeline for **Repo-Coding-Agent**.

Maybe in the next stage:

-  Add LLM tool use & MCP & functional call integration
-  Optimize history management and code block splitting (for optimizing long-context management)

Stage II: Refactor the code & add basic code splitting tools

Maybe in the next stage:

- Add MCP tools for refactoring again

- Add frontend components (HTML & CSS & JavaScripts)

## Todo List

- [x] Complete the most basic functional design. ✅
- [x] Complete basic file matching, filtering and walking class and util functions. ✅
- [x] Complete the refactoring for the repo code structure for making it available as a python package. ✅
- [x] Complete the basic context management for stage one. ✅
- [x] Complete the model response. ✅
- [x] Couple the two modules and build the final pipeline. ✅
- [x] !REFACTOR: Remove camel. ✅
- [x] !REBUILD: Developing a simple and lightweight LLM multi-turn conversation mini-app with history management. ✅
    - [ ] Complete basic model history management
    - [x] Figure out how mainstream LLMs manage history records
- [x] Add basic python parser using `ast`. ✅
    - [ ] Debug and add more functions for analyzing the tools
    - [ ] Integrate this independent modules into pipeline
    - [ ] View this as a MCP tool calling and refactor the code again
- [ ] MCP configuration
    - [x] Finish MCP tools settings
    - [ ] Finish MCP prompts settings
    - [ ] Finish MCP resources settings
    - [ ] Finish MCP Sampling
    - Relevant Web: [MCP Components](https://huggingface.co/learn/mcp-course/en/unit1/key-concepts)

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
│   │   ├── agent.py
│   │   ├── client_utils.py
│   │   ├── config.json
│   │   ├── mcp_tool_integrate.py
│   │   ├── prompt.py
│   │   └── tools
│   │       ├── file_ops.py
│   │       └── web_search.py
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
