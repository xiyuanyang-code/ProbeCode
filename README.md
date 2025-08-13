# Repo-Coding Agent

> [!WARNING]
> This repo is still in construction process
> To be refactored

## Introduction

We aim to create a **Repo Coding Agent** specializing in understanding extremely long and complex code blocks (even those exceeding the context length of an LLM). This agent will effectively read the relevant specialized code sections, thereby enhancing the LLM's code comprehension and generation capabilities for the given problem.

> It is just a toy implementation...

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
- [x] Couple the two modules and build the final pipeline
- [ ] !REFACTOR: Remove camel
- [ ] !REBUILD: Developing a simple and lightweight LLM multi-turn conversation mini-app with history management.
    - [ ] Complete basic model history management
    - [ ] Figure out how mainstream LLMs manage history records
- [x] Add basic python parser using `ast`. ✅
    - [ ] Debug and add more functions for analyzing the tools
    - [ ] Integrate this independent modules into pipeline
    - [ ] View this as a MCP tool calling and refactor the code again

## Structure

```bash
.
├── CodingAgent
│   ├── __init__.py
│   ├── agent.py                # basic agent class for managing LLM Response
│   ├── config.py               # loading basic config for LLM, including API key
│   ├── config.yaml             # config file, (gitignored)
│   ├── inspector
│   │   ├── __init__.py
│   │   ├── code_loader.py      # several functions for file typing matching and filtering
│   │   └── context_manager.py  # classes for managing what inspector will pass the code content to LLM
│   ├── llm
│   │   ├── __init__.py         
│   │   ├── history_manager.py  # managing history
│   │   ├── llm_client.py       # basic components for LLM client
│   │   └── prompt.py           # store basic prompt
│   ├── main.py                 # project entry point
│   └── utils
│       ├── __init__.py
│       └── logging_info.py     # modules for loggings
├── LICENSE
├── README.md
├── log
├── pyproject.toml
├── run.sh
└── test
    ├── __init__.py
    ├── test_inspector.py       # unit test for inspector 
    └── test_walk_file.py       # test for matching file types and walking
```