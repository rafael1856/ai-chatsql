"""
This module provides configuration and setup for logging within the AI Database Chatbot project.

The module includes functions for:
- Setting up a logger with a specified log level.
- Loading the log level from a JSON configuration file.
- Configuring the logger based on the log level specified in a given file.

The logger is configured to write logs to a file named 'application.log' by default. The log level can be adjusted to control the verbosity of the logging output.

Usage:
    To configure the logger, import the module and call the `configure_logger_from_file` function with the path to your log configuration file.

    Example:
        from logger_config import configure_logger_from_file
        logger = configure_logger_from_file('path/to/config.json')

Dependencies:
    - Python's built-in `logging` module.
    - A JSON configuration file specifying the log level.
"""

import logging
import os
import json


def setup_logger(log_level,log_title:str=None):
    """
    Set up a logger with the specified log level.

    Args:
        log_level (int): The log level to be set for the logger.

    Returns:
        logging.Logger: The configured logger object.

    """
    # Create a logger
    logger = logging.getLogger(log_title)
    logger.setLevel(log_level)

    # Create a file handler
    handler = logging.FileHandler('logs/app.log')
    handler.setLevel(log_level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger

def load_log_level_from_file(file_name):
    """
    Loads the log level from a JSON configuration file.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        int: The log level as an integer value.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the JSON file is not valid.

    """
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the full path to the config.json file
    file_path = os.path.join(dir_path, file_name)

    print(f"Loading log level from file: {file_path}")

    # with open(file_path, 'r', encoding="utf-8") as file:
    with open(file_path, 'r') as file:
        config = json.load(file)
        return logging.getLevelName(config['log_level'])

def configure_logger_from_file(file_path):
    """
    Configures the logger based on the log level specified in the given file.

    Args:
        file_path (str): The path to the file containing the log level configuration.

    Returns:
        logger: The configured logger object.
    """
    log_level = load_log_level_from_file(file_path)
    logger = setup_logger(log_level)
    return logger
