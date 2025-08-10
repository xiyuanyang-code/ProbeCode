import os
import sys
import argparse
from typing import List, Tuple
from rich.console import Console

# todo add prompt toolkit

sys.path.append(os.getcwd())

from camel.memories.records import MemoryRecord
from camel.messages import BaseMessage
from camel.types import OpenAIBackendRole

from CodingAgent.inspector.context_manager import FileContentReader
from CodingAgent.llm.memory_manager import ChatHistoryManager
from CodingAgent.llm.llm_agent import CodingAgent
from CodingAgent.utils.logging_info import setup_logging_config


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


def chat_loop(
    system_message: str,
    initial_query: str = "Hello, can you help me explain this project?",
):
    """
    Runs a chat interaction with the coding agent.

    Args:
        system_message: The system message to initialize the agent with.
        initial_query: The initial query to send to the agent.
    """
    coding_agent = CodingAgent(system_message=system_message)
    history_manager = ChatHistoryManager()
    console = Console()

    # Initial interaction
    history_manager.add_user_message(
        f"This is the code to be analyzed: {system_message}"
    )
    print("Agent:", end=" ")
    # initial_query += system_message
    print(initial_query)
    initial_response = coding_agent.step(initial_query)
    initial_response_content = initial_response.msgs[0].content
    print(initial_response_content)
    history_manager.add_user_message(initial_query)
    history_manager.add_agent_message(initial_response_content)

    # Begin the loop
    while True:
        user_command: str = console.input(
            "[bold yellow]Input your command: [/bold yellow]"
        ).strip()
        if user_command.lower() in ["/exit", "/quit"]:
            break

        # Get history summary and send with new user command
        history_summary = history_manager.get_history_summary()
        response = coding_agent.step(
            input_message=f"Current user command: {user_command}\n\nHistory:{history_summary}"
        )
        response_content = response.msgs[0].content

        print("Agent:", end=" ")
        print(response_content)

        history_manager.add_user_message(user_command)
        history_manager.add_agent_message(response_content)

        # print(f"Get History Summary: \n{history_manager.get_history_summary()}")


def main():
    """Main function to run the coding agent service."""
    logger.info("[MAIN]: STARTING SERVICE")
    args_dict = parsing_arguments()
    project_context = get_project_context(args_dict["project_path"])
    chat_loop(system_message=project_context)
    logger.info("[MAIN]: ENDING SERVICE")


if __name__ == "__main__":
    main()
