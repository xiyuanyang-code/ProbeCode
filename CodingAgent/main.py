import os
import sys
import argparse
from typing import List, Tuple
from rich.console import Console
import asyncio

# todo add refactored llm response components

sys.path.append(os.getcwd())

from CodingAgent.inspector.context_manager import FileContentReader
from CodingAgent.config import load_config
from CodingAgent.utils.log import setup_logging_config
from CodingAgent.utils.greetings import welcome, goodbye
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
        # todo initialize a small LLM to automatically change this
        # this is just for the default settings
        include_list=["*.py"],
        exclude_list=["*/log/*", "*/build/*", "dist/*, .venv/*"],
    ) as context_manager:
        contents: List[Tuple[str, str]] = context_manager.get_content()

    for path, content in contents:
        system_message += (
            f"\n\nFile: {path}\n\n=====BEGIN=====\n{content}\n=====END=====\n"
        )
    return str(system_message), contents


async def main_():
    """Main function to run the coding agent service."""
    console = Console()
    config = load_config()
    logger.info("[MAIN]: STARTING SERVICE")

    # section1: parse args
    # todo remove argparse, we recommend you to run this file in current working directory
    args_dict = parsing_arguments()
    console.print(f"[purple]{welcome()}[/purple]")

    # section2: data preprocessing for environment setup
    console.print("[purple]Loading environments for ProbeCode...[/purple]")
    # project_context = get_project_context(args_dict["project_path"])

    # section3: initializing MCP chatbot
    console.print("[purple]ProbeCode Agent is coming...[/purple]")
    chatbox = MCPChat(
        config_file=os.path.join(
            config.get("default_dir"), "CodingAgent/llm/config.json"
        )
    )
    await chatbox.connect(server_name="tools")

    # section4: ending chat
    console.print(f"[purple]{goodbye()}[/purple]")
    logger.info("[MAIN]: ENDING SERVICE")


def main():
    asyncio.run(main_())


if __name__ == "__main__":
    print("We recommend you to run this project via pip")
    asyncio.run(main_())
