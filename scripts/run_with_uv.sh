#!/bin/bash

pip install pyyaml

# get some preliminaries
python -m CodingAgent.config

# remove caches
rm -rf ./build
rm -rf ./dist
rm -rf CodingAgent.egg-info

# RECOMMEND RUNNING WITH UV
uv venv
uv sync

source .venv/bin/activate
