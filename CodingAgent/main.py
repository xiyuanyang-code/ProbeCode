"""Main module for the Coding Agent application."""
import os
import sys
import argparse

sys.path.append(os.getcwd())

from CodingAgent.inspector.context_manager import FileContentReader
from CodingAgent.llm.llm_agent import CodingAgent
from CodingAgent.utils.logging_info import setup_logging_config

logger = setup_logging_config()


def parsing_arguments():
    """Parse command-line arguments.
    
    Returns:
        dict: A dictionary containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="A coding agent that helps with code understanding.")
    parser.add_argument(
        "--project_path",
        type=str,
        default=os.getcwd(),
        help="The project location, absolute path is recommended.",
    )
    # TODO: Add fix for relative location

    args = parser.parse_args()
    return vars(args)


def main():
    """Main function to run the coding agent service."""
    logger.info("[MAIN]: STARTING SERVICE")
    args_dict = parsing_arguments()

    # Get file content
    # TODO: It is just a simple situation, we will optimize it in the near future
    file_path = args_dict["project_path"]
    with FileContentReader(
        file_path=file_path,
        include_list=["*.py"],
        exclude_list=["log/*", "build/*", "dist/*", "test/*"],
    ) as context_manager:
        contents = context_manager.get_content()

    # Get the system message
    # TODO: Add files filtering and more flexible control
    system_message: str = "You are good at coding"
    for path, content in contents:
        system_message += f"The file: {path} has the following content: \n\n =====BEGIN===== \n{content}\n =====END===== \n\n"

    # Chat loop
    # TODO: Add multi-turn chat loop
    chat_loop(system_message=system_message)
    logger.info("[MAIN]: ENDING SERVICE")


def chat_loop(
    initial_query: str = "Hello, can you help me explain this project?",
    system_message: str = "Hello!",
):
    """Run a single chat interaction with the coding agent.
    
    Args:
        initial_query: The initial query to send to the agent.
        system_message: The system message to initialize the agent with.
    """
    coding_agent = CodingAgent(system_message=system_message)
    print(coding_agent.step(initial_query).msgs[0].content)


if __name__ == "__main__":
    main()

