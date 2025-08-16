"""Utility functions for LLM client configuration."""
import os
import sys

sys.path.append(os.getcwd())

from CodingAgent.utils.log import setup_logging_config

logger = setup_logging_config()


def load_apikey_config():
    """Load the API key and base URL from environment variables.

    Returns:
        tuple: (api_key, base_url) where
            api_key (str or None): The API key from the environment variable 'OPENAI_API_KEY'.
            base_url (str or None): The base URL from the environment variable 'BASE_URL'.

    Logs:
        Logs the loading process and warns if any variable is missing.
    """
    api_key = os.getenv("ZHIPU_API_KEY")
    base_url = os.getenv("ZHIPU_API_BASE_URL")
    if api_key:
        logger.info("OPENAI_API_KEY loaded successfully.")
    else:
        logger.warning("OPENAI_API_KEY is not set in environment variables.")
    if base_url:
        logger.info("BASE_URL loaded successfully.")
    else:
        logger.warning("BASE_URL is not set in environment variables.")

    return api_key, base_url


if __name__ == "__main__":
    print(load_apikey_config())
