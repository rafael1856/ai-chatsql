"""
helper_functions.py

This module contains utility functions for the application. It includes a function 
for saving a conversation history to a markdown file.

Functions:
    save_conversation(conversation_history, directory="conversation_history"): 
    Saves a given conversation history to a markdown file with timestamps. Each message 
    in the conversation history is written to the file with a timestamp, a role icon 
    (🧑‍💻 for user, 🤖 for assistant), the role title, and the message content.

Imports:
    os: Provides functions for interacting with the operating system.
    datetime: Provides functions for working with dates and times.
    logger_config: Contains the function for configuring the logger.

Variables:
    logger: The logger configured from a JSON file.
"""

import os
import datetime
from logger_config import configure_logger_from_file

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

def save_conversation(conversation_history, directory="conversation_history"):
    """
    Save the conversation history to a file.

    Args:
        conversation_history (list): The list of messages in the conversation.
        directory (str, optional): The directory where the conversation file will be saved. Defaults to "conversation_history".

    Returns:
        str: The file path of the saved conversation.

    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the current date and time for the filename
    current_datetime = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    file_path = os.path.join(directory, f"{current_datetime}.md")

    with open(file_path, 'w', encoding='utf-8') as file:
        for message in conversation_history:
            if message["role"] in ["user", "assistant"]:
                message_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                role_icon = '🧑‍💻' if message["role"] == "user" else '🤖'
                file.write(f"{message_timestamp} **{role_icon} {message['role'].title()}:** {message['content']}\n\n")
    return file_path

