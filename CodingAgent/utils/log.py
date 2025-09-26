"""Logging configuration for the coding agent."""

import logging
import os
import sys
import colorlog

sys.path.append(os.getcwd())

from CodingAgent.config import load_config
config = load_config()


# add notice level
NOTICE_LEVEL = 25
logging.addLevelName(NOTICE_LEVEL, "NOTICE")


def notice(self, message, *args, **kwargs):
    """Adds a notice method to the logger for consistency."""
    if self.isEnabledFor(NOTICE_LEVEL):
        self._log(NOTICE_LEVEL, message, args, **kwargs)


logging.Logger.notice = notice
SHARED_LOGGER_NAME = "CodingAgent"


def _create_file_handler(logger: logging.Logger, formatter: logging.Formatter):
    """
    Attempts to create and configure a file handler for the logger.
    If it fails (e.g., due to permission errors), it logs the error and returns None.
    """
    log_dir = config.get("log_dir")
    if not log_dir:
        logger.error("Configuration key 'log_dir' is missing.")
        return None

    log_file_path = os.path.join(log_dir, "Agent.log")

    try:
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return file_handler
    except OSError as e:
        logger.error(
            f"Failed to create or write to log file at '{log_dir}'. File logging will be disabled. Error: {e}"
        )
        return None


def _create_console_handler(logger: logging.Logger, formatter: logging.Formatter):
    """
    Creates and configures a console handler for the logger.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(NOTICE_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return console_handler


def setup_logging_config():
    """
    Sets up logging configuration by creating file and console handlers.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(SHARED_LOGGER_NAME)
    # Return the existing logger to prevent adding duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s]: %(message)s")
    colored_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)s [%(name)s]: %(message)s%(reset)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "white",
            "INFO": "white",
            "NOTICE": "bold_white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    _create_file_handler(logger, formatter)
    _create_console_handler(logger, colored_formatter)

    return logger


# --- Validation Section ---
if __name__ == "__main__":
    logger = setup_logging_config()
    logger.info("This is an info message. It will NOT be visible on the console.")
    logger.notice("This is a notice message, it WILL be visible on the console.")
    logger.warning("This is a warning message.")
    logger.debug("This is a debug message, it will NOT be visible on the console.")
