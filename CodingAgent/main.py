import os
import sys
import argparse
from typing import List, Tuple
from rich.console import Console
import asyncio

# todo add refactored llm response components

sys.path.append(os.getcwd())

from CodingAgent.inspector.context_manager import FileContentReader
from CodingAgent.utils.log import setup_logging_config
from CodingAgent.llm.agent.client_chat import MCPChat


logger = setup_logging_config()


def parsing_arguments():
    """Parse command-line arguments.

    Returns:
        dict: A dictionary containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="A coding agent that helps with code understanding."
    )
    parser.add_argument(
        "--project_path",
        type=str,
        default=os.getcwd(),
        help="The project location, absolute path is recommended.",
    )
    args = parser.parse_args()
    return vars(args)


def get_project_context(project_path: str) -> str:
    """
    Reads project files and returns their content as a single string.

    Args:
        project_path: The root path of the project.

    Returns:
        str: A formatted string containing the content of all relevant files.
    """
    system_message = "You are good at coding."
    with FileContentReader(
        file_path=project_path,
        include_list=["CodingAgent/*.py"],
        exclude_list=["log/*", "build/*", "dist/*", "test/*, CodingAgent/llm/*"],
    ) as context_manager:
        contents: List[Tuple[str, str]] = context_manager.get_content()

    for path, content in contents:
        system_message += (
            f"\n\nFile: {path}\n\n=====BEGIN=====\n{content}\n=====END=====\n"
        )
    return str(system_message)


async def main():
    """Main function to run the coding agent service."""
    logger.info("[MAIN]: STARTING SERVICE")
    args_dict = parsing_arguments()
    project_context = get_project_context(args_dict["project_path"])
    chatbox = MCPChat(
        config_file="/home/xiyuanyang/Agents/Coding_Agent/CodingAgent/llm/config.json"
    )
    await chatbox.connect(server_name="tools")
    logger.info("[MAIN]: ENDING SERVICE")


if __name__ == "__main__":
    asyncio.run(main())
