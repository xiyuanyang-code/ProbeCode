#!/bin/bash

# get some preliminaries
python -m CodingAgent.config

# clear some cache
rm -rf ./build
rm -rf ./dist
rm -rf CodingAgent.egg-info

python -m build
pip install . --force-reinstall

# or for debugging mode: use pip install -e .