import os
import sys
import json
from typing import List, Dict, Union
import datetime
from anthropic import Anthropic, APIStatusError
from anthropic.types import ToolUseBlock, Message

sys.path.append(os.getcwd())

from CodingAgent.config import load_config


class MemoryManager:
    """
    Manages the short-term and long-term memory for a chatbot.

    This class handles the core logic for storing, summarizing, and retrieving
    dialogue history. It implements a two-tiered memory system:
    - **Short-Term Memory (STM):** Stores recent, detailed conversation turns.
      This is the primary context for the LLM.
    - **Long-Term Memory (LTM):** Stores compressed summaries of past conversations.
      This is used to maintain high-level context over long dialogues.

    Additionally, this manager provides a mechanism for real-time, persistent
    storage of the chat history to a timestamped file on disk.
    """

    def __init__(self, config: Dict, llm_client: Anthropic):
        """
        Initializes the MemoryManager with an empty memory and file storage.

        Args:
            config (Dict): A dictionary containing configuration settings,
                           e.g., the short-term memory threshold.
            llm_client (Anthropic): An instance of the Anthropic client,
                                    used for memory summarization.
        """
        self.short_term_memory: List[Dict] = []
        self.long_term_memory: List[Dict] = []
        self.config = load_config()

        self.short_term_memory_threshold = config.get("memory", {}).get(
            "short_term_threshold", 50
        )

        self.llm_client = llm_client

        # New feature: persistent history file management
        self.history_dir = os.path.join(self.config.get("default_dir"), "./history")
        os.makedirs(self.history_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.history_file_path = os.path.join(
            self.history_dir, f"chat_history_{timestamp}.json"
        )
        self._save_history_to_file()

    def _summarize_memory(self, messages_to_summarize: List[Dict]) -> str:
        """
        Uses an LLM to generate a concise summary of a list of messages.

        This method sends the formatted dialogue to the LLM with a specific
        prompt to create a summary, which is then stored in long-term memory.

        Args:
            messages_to_summarize (List[Dict]): The list of messages from
                                                short-term memory to be summarized.

        Returns:
            str: The summarized text of the conversation. Returns a fallback
                 message if the summarization fails due to an API error.
        """
        summary_prompt = [
            {
                "role": "user",
                "content": "Please provide a concise summary of the following conversation, extracting only the key information and main points. Return only the summary content, without any additional embellishments.",
            },
            {
                "role": "assistant",
                "content": f"Conversation content:\n{self._format_messages(messages_to_summarize)}",
            },
        ]

        try:
            response = self.llm_client.messages.create(
                max_tokens=512,
                model="claude-3-haiku-20240307",
                messages=summary_prompt,
            )
            return response.content[0].text
        except APIStatusError as e:
            print(f"Failed to summarize memory: {e.response.text}")
            return "Fail to summarize"

    def _format_messages(self, messages: List[Dict]) -> str:
        """
        Formats a list of message dictionaries into a readable string.

        This is a helper method that correctly handles and serializes various
        content types, including simple strings and complex Anthropic API objects
        like ToolUseBlock, ensuring the output is suitable for LLM processing.

        Args:
            messages (List[Dict]): The list of message dictionaries to format.

        Returns:
            str: A formatted string representation of the conversation.
        """
        formatted_str = ""
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if not content:
                continue

            formatted_str += f"{role}: \n"

            if not isinstance(content, list):
                content = [content]

            for item in content:
                if isinstance(item, ToolUseBlock):
                    formatted_str += f"  Calling tool '{item.name}' with args: {json.dumps(item.input)}\n"
                else:
                    # Fallback to string representation for other content types
                    formatted_str += f"  {str(item)}\n"

        return formatted_str.strip()

    def _save_history_to_file(self):
        """
        Saves the current state of both long-term and short-term memory
        to the persistent history file.

        This method is called after every significant memory update to
        ensure the conversation history is continuously backed up.
        Unserializable objects are converted to strings before saving.
        """
        full_history = {
            "long_term_memory": self.long_term_memory,
            "short_term_memory": self.short_term_memory,
        }
        try:
            with open(self.history_file_path, "w", encoding="utf-8") as f:
                json.dump(full_history, f, indent=4, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Failed to save chat history to file: {e}")

    def add_message(self, message: Dict):
        """
        Adds a new message to the short-term memory and triggers a save.

        Args:
            message (Dict): The new message dictionary to be added.
        """
        self.short_term_memory.append(message)
        self._save_history_to_file()

    def get_full_context(self) -> List[Dict]:
        """
        Retrieves the complete conversation context for the LLM.

        This method combines the long-term memory and short-term memory.
        It also checks if the short-term memory has reached its compression
        threshold and triggers the summarization process if necessary.

        Returns:
            List[Dict]: A list of message dictionaries representing the
                        full conversation context.
        """
        if len(self.short_term_memory) >= self.short_term_memory_threshold:
            print("Short-term memory threshold reached. Summarizing...")
            summary = self._summarize_memory(self.short_term_memory)
            self.long_term_memory.append(
                {
                    "role": "user",
                    "content": f"Historical conversation summary: {summary}",
                }
            )
            # The short-term memory is cleared after summarization
            self.short_term_memory = []
            print("Memory summarized and updated.")

        # Save the updated history after potential summarization
        self._save_history_to_file()

        return self.long_term_memory + self.short_term_memory

    def store_short_term_memory(self):
        """
        Manually transfers the current short-term memory to long-term memory.

        This action bypasses the summarization process, allowing the full,
        uncompressed dialogue to be preserved. This is useful for saving
        important context as requested by the user.
        """
        summary_text = (
            "User requested to save the following conversation content:\n"
            + self._format_messages(self.short_term_memory)
        )
        self.long_term_memory.append({"role": "user", "content": summary_text})

        self.short_term_memory = []
        self._save_history_to_file()

    def reset_memory(self):
        """
        Resets both short-term and long-term memory, effectively starting
        a new conversation from scratch. The history file is also cleared.
        """
        self.short_term_memory = []
        self.long_term_memory = []
        self._save_history_to_file()
