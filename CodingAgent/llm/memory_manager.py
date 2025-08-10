from camel.memories.records import MemoryRecord
from camel.messages import BaseMessage
from camel.types import OpenAIBackendRole
from camel.memories.blocks import ChatHistoryBlock
from typing import List
from CodingAgent.utils.logging_info import setup_logging_config


logger = setup_logging_config()


class ChatHistoryManager:
    """Manages the chat history for the coding agent."""

    def __init__(self, max_history_window: int = -1):
        """
        Initializes the ChatHistoryManager.

        Args:
            max_history_size: The maximum number of turns to keep in the history, set -1 for no restrictions
        """
        self.history = ChatHistoryBlock()
        self.max_history_size = max_history_window

    def add_user_message(self, content: str):
        """Adds a user message to the history."""
        self.history.write_record(
            MemoryRecord(
                message=BaseMessage.make_user_message(
                    role_name="user", content=content
                ),
                role_at_backend=OpenAIBackendRole.USER,
            )
        )

    def add_agent_message(self, content: str):
        """Adds an agent message to the history."""
        self.history.write_record(
            MemoryRecord(
                message=BaseMessage.make_assistant_message(
                    role_name="assistant", content=content
                ),
                role_at_backend=OpenAIBackendRole.ASSISTANT,
            )
        )

    def get_history_summary(self) -> str:
        """
        Returns a summary of the chat history.

        Returns:
            str: A string representation of the recent chat history.
        """
        # todo use a small agent or other techniques to optimize history managing
        return self.history.retrieve(window_size=5)

