import os
import sys
import aiofiles

sys.path.append(os.getcwd())

import importlib
import inspect
from mcp.server.fastmcp import FastMCP
from CodingAgent.config import load_config


# Create a single MCP server instance with a name.
mcp = FastMCP("all_tools")


def get_tool_modules_from_directory(directory: str) -> list[str]:
    """
    Scans a directory for Python files and returns a list of their module names.
    """
    module_names = []
    # List all files in the specified directory.
    for filename in os.listdir(directory):
        # Check if the file is a Python file and not a special file like __init__.py.
        if filename.endswith(".py") and not filename.startswith("__"):
            # Construct the module name (e.g., 'web_search' from 'web_search.py').
            module_name = filename[:-3]
            module_names.append(f"{directory}.{module_name}")
    return module_names


def register_tools_from_modules(module_list: list[str]):
    """
    Dynamically imports and registers all functions from a list of tool modules.
    """
    for module_name in module_list:
        try:
            # Dynamically import the module by name.
            module = importlib.import_module(module_name)

            # Iterate through all members of the module.
            for name, func in inspect.getmembers(module, inspect.isfunction):
                # Use the mcp.tool() decorator to register the function as a tool.
                mcp.tool()(func)
            print(f"Successfully registered tools from module: {module_name}")
        except ImportError as e:
            print(f"Failed to import module '{module_name}': {e}")
        except Exception as e:
            print(
                f"An error occurred while registering tools from '{module_name}': {e}"
            )


if __name__ == "__main__":
    # Get the list of modules by scanning the 'tools' directory.
    config = load_config()
    default_dir = config.get("default_dir")
    tools_directory = os.path.join(default_dir, "CodingAgent/llm/tools")
    print(tools_directory)
    tool_modules = get_tool_modules_from_directory(tools_directory)

    tool_modules_ = [
        ("tools." + tool_module.rsplit(".", 1)[-1]) for tool_module in tool_modules
    ]

    # Register the found tools.
    register_tools_from_modules(tool_modules_)

    # Finally, run the single MCP server with the standard I/O transport.
    mcp.run(transport="stdio")
