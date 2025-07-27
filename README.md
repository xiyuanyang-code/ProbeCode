# Repo-Coding Agent

> [!WARNING]
> This repo is still in construction process

## Current Constructing

Stage I: We want to let LLM accept the full content for all lines of code of the repository, which can better improve the comprehension of overall code for LLM.

We need to implement:

- Show full context for large-language models.

- Add history management for multi LLM response.

- Finish the basic running pipeline for **Repo-Coding-Agent**.

Maybe in the next stage:

-  Add LLM tool use & MCP & functional call integration
-  Optimize history management and code block splitting (for optimizing long-context management)

## Todo List

- [x] Complete the most basic functional design. ✅
- [x] Complete basic file matching, filtering and walking class and util functions. ✅
- [x] Complete the refactoring for the repo code structure for making it available as a python package. ✅
- [x] Complete the basic context management for stage one. ✅
- [ ] Complete the model response.
- [ ] Complete basic model history management
- [ ] Figure out how mainstream LLMs manage history records
- [ ] Couple the two modules and build the final pipeline

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