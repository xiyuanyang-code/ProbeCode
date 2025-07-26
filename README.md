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


## Structure

```bash
.
├── README.md
├── agent.py                # basic agent class for managing LLM Response
├── config.py               # loading basic config for LLM, including API key
├── inspector               # package1: the inspector for inspecting codes
│   ├── __init__.py 
│   ├── code_loader.py      # loading codes for different file types and ignoring some certain files 
│   └── context_manager.py  # managing what inspector will be passed to the LLM
├── llm
│   ├── __init__.py
│   ├── history_manager.py  # managing history
│   ├── llm_client.py       # basic components for LLM client
│   └── prompt.py           # store basic prompt
├── main.py
├── test
│   ├── __init__.py
│   └── test_inspector.py   # some initial unit test
└── utils
    ├── __init__.py
    ├── file_utils.py       # utils for loading files
    └── logging_info.py     # recording loggings
```

