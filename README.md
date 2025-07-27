# Coding Agent

> [!WARNING]
> This repo is still in construction process

## Current Constructing

Stage I: We want to let LLM accept the full content for all lines of code of the repository, which can better improve the comprehension of overall code for LLM.

We need to implement:

- Show full context for large-language models.

- Add history management for multi LLM response.

## Todo List

- [ ] Add basic component: show full context for large language models

- [ ] Add Basic LLM-response pipeline

- [ ] Add LLM tool use (Optional)

- [ ] Add diff for modification (Optional)

## What I have finished 😊

- ✅: Finish basic file matching, filtering and walking class and util functions

- ✅: refactor file structure for making it can be installed via `pip install .`

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

10 directories, 30 files
```