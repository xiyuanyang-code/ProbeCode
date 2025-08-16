# base_chat.py
import os
import sys
import json
import asyncio
from typing import Dict, List

sys.path.append(os.getcwd())

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import PromptSession

from CodingAgent.utils.log import setup_logging_config


class UserChat:
    """
    Handles user input and output interactions using prompt_toolkit.
    This class is responsible for the UI layer of the chatbot.
    """

    def __init__(self):
        self.session = PromptSession(history=FileHistory(".history.txt"))

    def get_input(self):
        """
        Asynchronously gets user input with an interactive prompt.
        """
        try:
            user_input = self.session.prompt(
                "Input your message: ", auto_suggest=AutoSuggestFromHistory()
            )
            return str(user_input).strip()
        except KeyboardInterrupt:
            # Handle Ctrl-C to gracefully exit the chat
            return "/exit"

    def display_output(self, message: str):
        """
        Displays a message to the user.
        """
        print(message)

    def display_system_message(self, message: str):
        """
        Displays a system message (e.g., info, warning) to the user.
        """
        print(f"[SYSTEM] {message}")


class BaseChat:
    """
    A base class for implementing a multi-turn chat with an LLM.
    Handles core chat loop, message management, and configuration loading.
    """

    def __init__(self, config_file: str = "config.json"):
        self.logger = setup_logging_config()
        self.config: Dict = self._load_config(config_file)
        self.llm_client = None
        self.available_tools: List[Dict] = []
        self.user_chat = UserChat()

    def _load_config(self, file_path: str) -> Dict:
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from '{file_path}' successfully.")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file '{file_path}' not found.")
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(
                f"Failed to parse configuration from '{file_path}'. Details: {e}"
            )
        return {}

    async def _process_query(self, query: str):
        raise NotImplementedError(
            "Subclasses must implement the _process_query method."
        )

    async def chat_loop(self):
        """
        Runs an interactive chat loop using the UserChat instance.
        """
        self.logger.notice("\nChatbot Started!")
        self.logger.notice("Type your queries or '/exit' to exit.")
        while True:
            try:
                # Use the new UserChat instance to get input
                query = self.user_chat.get_input()

                if query == "/exit" or query.lower() == "quit":
                    self.logger.notice("Exiting chat loop.")
                    break

                if not query:
                    continue

                await self._process_query(query)

            except Exception as e:
                self.logger.error(f"An error occurred during chat loop: {str(e)}")
