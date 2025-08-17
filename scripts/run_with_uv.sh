#!/bin/bash
# --- Preparation ---
# Ensure the script exits immediately if any command fails
echo "--- Setting up environment for ProbeCode ---"

# Install necessary tools
pip install pyyaml

# Perform initial configuration
python -m CodingAgent.config

# Clean up old build files
echo "Cleaning up old build and dist files..."
rm -rf ./build ./dist CodingAgent.egg-info

# --- uv environment setup ---
# Check if the uv command exists
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' command not found. Please install it first."
    echo "To install: pip install uv"
    exit 1
fi

# Check the current default Python version
echo "Checking default Python version..."
PYTHON_PATH=$(which python3 || which python)

# Ensure a Python executable was found
if [ -z "$PYTHON_PATH" ]; then
    echo "Error: No 'python3' or 'python' executable found in your PATH."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_PATH -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

# Check if the version is greater than or equal to 3.10
if awk -v ver="$PYTHON_VERSION" 'BEGIN {exit !(ver >= 3.10)}'; then
    echo "Found compatible Python version: $PYTHON_VERSION"
    echo "Creating virtual environment with uv using $PYTHON_PATH..."
    uv venv -p "$PYTHON_PATH"
else
    echo "Warning: Default Python version is $PYTHON_VERSION, which is less than 3.10."
    echo "Skipping -p argument. uv will use its default Python."
    uv venv
fi


# Install dependencies
echo "Installing project dependencies with uv..."
uv pip install -r pyproject.toml
echo "Setup complete. Virtual environment"

pip install -e .