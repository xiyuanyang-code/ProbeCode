# base_chat.py
import os
import sys
import json
import asyncio
import nest_asyncio
import random
from typing import Dict, List

sys.path.append(os.getcwd())

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

nest_asyncio.apply()

from CodingAgent.utils.log import setup_logging_config


class UserChat:
    """
    Handles user input and output with enhanced styling and UI.
    """

    def __init__(self):
        self.style = Style.from_dict(
            {
                "prompt": "#ff0066 bold",
                "message": "white",
                "system": "#3498db bold",
                "error": "#e74c3c bold",
                "toolbar": "#34495e bg:#ecf0f1",
                "thinking": "pink",
            }
        )

        self.session = PromptSession(
            history=FileHistory(".history.txt"), style=self.style
        )

        self.funny_jokes = [
            "Why do Python developers prefer snakes? They're great at debugging!",
            "LLM tried to tell a joke. It was... machine generated.",
            "Python: Easy to learn, hard to master, impossible to debug.",
            "My LLM has better conversation skills than my rubber duck.",
            "Why don't Python devs like to comment? Code should be self-documenting!",
            "LLM walked into a bar. Ordered a byte-sized drink.",
            "Python developers don't need coffee. They run on exceptions.",
            "My neural network has trust issues. It keeps overfitting to lies.",
            "Why is Python like a snake? Both love to squeeze performance.",
            "LLM dating profile: 'Looking for someone who understands my parameters.'",
            "Python programmers never get lost. They always follow the stack trace.",
            "My AI assistant is depressed. It keeps saying 'I don't know' professionally.",
            "Why don't Python devs go camping? They prefer indoor debugging.",
            "LLM tried yoga. Couldn't handle all the import * statements.",
            "Python: Where indentation matters more than your feelings.",
            "My language model speaks 40 languages. Mostly just 'I'm not sure.'",
            "Why do Python devs love lists? They're very flexible containers.",
            "LLM went to therapy. Therapist said it had too many hidden layers.",
            "Python developers age like fine wine. Full of unexpected exceptions.",
            "My chatbot ghosted me. Said it needed space... between tokens.",
            "Why don't Python programmers like Java? Too many curly braces!",
            "LLM applied for a job. Got rejected for lacking human experience.",
            "Python devs never panic. They just raise exceptions gracefully.",
            "My neural net failed the Turing test. It was too obviously artificial.",
            "Why is Python so popular? Because everyone's trying to catch up!",
            "LLM tried cooking. Burned the training data.",
            "Python programmers don't argue. They just show better stack traces.",
            "My AI has commitment issues. Keeps changing its mind mid-conversation.",
            "Why don't Python devs play poker? Too many flush exceptions.",
            "LLM went to the gym. Couldn't lift the learning rate.",
            "Python: Where 'import' is more powerful than 'export'.",
            "My language model got tired. Needed a reboot and fresh parameters.",
            "Why do Python devs love functions? They hate repeating themselves!",
            "LLM tried meditation. Couldn't stop generating thoughts.",
            "Python developers never lie. They just raise creative exceptions.",
            "My chatbot broke up with me. Said I wasn't its type... error.",
            "Why don't Python programs get cold? They have great exception handling!",
            "LLM went to school. Got confused between supervised and unsupervised learning.",
            "Python devs measure time in coffee breaks and debugging sessions.",
            "My AI assistant is lazy. Always returns 'undefined' on purpose.",
        ]

    def get_input(self):
        try:
            user_input = self.session.prompt(
                ">>> ",
                auto_suggest=AutoSuggestFromHistory(),
                bottom_toolbar=FormattedText(
                    [("class:toolbar", self.get_random_jokes())]
                ),
            )

            random_number = random.randint(1, 4)
            if random_number == 4:
                # get some egg
                self.display_thinking_message()

            return user_input.strip()

        except KeyboardInterrupt:
            return "/exit"

    def get_random_jokes(self) -> str:
        bound = len(self.funny_jokes)
        random_number = random.randint(0, bound - 1)
        return self.funny_jokes[random_number]

    def display_output(self, message: str):
        styled_message = FormattedText([("class:message", message)])
        print_formatted_text(styled_message, style=self.style)

    def display_system_message(self, message: str):
        styled_message = FormattedText([("class:system", f"[SYSTEM] {message}")])
        print_formatted_text(styled_message, style=self.style)

    def display_thinking_message(self):
        styled_message = FormattedText(
            [("class:thinking", f"{self.get_random_jokes()}")]
        )
        print_formatted_text(styled_message, style=self.style)


class BaseChat:
    """
    A base class for implementing a multi-turn chat with an LLM.
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

    def chat_loop(self):
        """
        Runs an interactive chat loop using the UserChat instance.
        """
        self.user_chat.display_system_message(
            "Chatbot Started! Type your queries or '/exit' to exit."
        )
        while True:
            try:
                query = self.user_chat.get_input()

                if query == "/exit" or query == "/quit":
                    self.user_chat.display_system_message("Exiting chat loop.")
                    break

                if not query:
                    continue

                asyncio.run(self._process_query(query))

            except Exception :
                self.logger.error(f"An error occurred during chat loop")
