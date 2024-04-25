"""
chat_functions.py

This module contains functions for handling chat operations in the application. 
It includes a function for running a chat sequence with given messages and functions.

Imports:
    tiktoken: A Python library for counting tokens in a text string.
    streamlit: Framework for creating web apps with Python.
    config: Contains the AI model configuration.
    api_functions: Contains the `send_api_request_to_openai_api` and `execute_function_call` functions.
    logger_config: Contains the function for configuring the logger.

Variables:
    logger: The logger configured from a JSON file.

Functions:
    run_chat_sequence(messages, functions): Runs a chat sequence with the given messages and functions. 
    It returns the last message in the chat history.

The `run_chat_sequence` function takes two parameters: `messages`, which is a list of messages exchanged 
in the chat sequence, and `functions`, which is a dictionary of available functions. If the assistant 
message does not have a 'role' key, the function raises a KeyError.
"""

# Rest of the module code

import tiktoken
import streamlit as st
from config import AI_MODEL
from api_functions import send_api_request_to_openai_api, execute_function_call
from logger_config import configure_logger_from_file

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

def run_chat_sequence(messages, functions):
    """
    Runs a chat sequence with the given messages and functions.

    Args:
        messages (list): A list of messages exchanged in the chat sequence.
        functions (dict): A dictionary of available functions.

    Returns:
        dict: The last message in the chat history.

    Raises:
        KeyError: If the assistant message does not have a 'role' key.
    """
    logger.debug(f"Entering run_chat_sequence with messages: {messages}, functions: {functions}")
    if "live_chat_history" not in st.session_state:
        st.session_state["live_chat_history"] = [{"role": "assistant", "content": "Hello! I'm Andy, how can I assist you?"}]
        # st.session_state["live_chat_history"] = []

    internal_chat_history = st.session_state["live_chat_history"].copy()

    chat_response = send_api_request_to_openai_api(messages, functions)
    # assistant_message = chat_response.json()["choices"][0]["message"]
    assistant_message = chat_response.choices[0].message

# "message": {
#         "role": "assistant",
#         "content": " Hello! I'm Andy, an AI PostgreSQL SQL specialist. My purpose is to assist you with creating precise SQL scripts and running them. To get started, let me provide you with an overview of the available metrics in our database. Please find below a list:\n\n* Sales Volume by Product Category\n* Total Sales by Agent\n* Average Sale Price by Region\n* Customer Count by Age Group\n* Top 10 Customers by Spending\n\nPlease let me know which metric you would like to explore further."
#       },

    internal_chat_history.append({"role": assistant_message.role, "content": assistant_message.content})

        # # TODO remove this
    # internal_chat_history.append({"role": "user", "content": "You are a data analyst - provide personalized/customized explanations on what the results provided means and link them to the the context of the user query using clear, concise words in a user-friendly way. Or answer the question provided by the user in a helpful manner - either way, make sure your responses are human-like and relate to the initial user input. Your answers must not exceed 200 characters"})

    # chat_response = send_api_request_to_openai_api(internal_chat_history, functions)
    # assistant_message = chat_response.choices[0]["message"]

    if assistant_message.role == "assistant":
        st.session_state["live_chat_history"].append({"role": assistant_message.role, "content": assistant_message.content})

    results = st.session_state["live_chat_history"][-1]

    logger.debug(f"Exiting run_chat_sequence with last message:  {results}")
    print(f"Exiting run_chat_sequence with last message:{results}")

    return results

def clear_chat_history():
    """Clears the chat history stored in the Streamlit session state.

    This function removes the chat history stored in the Streamlit session state.
    It deletes the "live_chat_history", "full_chat_history", and "api_chat_history"
    variables from the session state.

    Parameters:
        None

    Returns:
        None

    """
    del st.session_state["live_chat_history"]
    del st.session_state["full_chat_history"]
    del st.session_state["api_chat_history"]

def count_tokens(text):
    """Count the total tokens used in a text string.

    Args:
        text (str): The input text string.

    Returns:
        int: The total number of tokens used in the text string.
    """
    logger.debug(f"Entering count_tokens with text: {text}")
    if not isinstance(text, str):
        return 0
    encoding = tiktoken.encoding_for_model(AI_MODEL)
    total_tokens_in_text_string = len(encoding.encode(text))
    logger.debug(f"Exiting count_tokens with total tokens: {total_tokens_in_text_string}")
    return total_tokens_in_text_string

def prepare_sidebar_data(database_schema_dict):
    """ 
    Prepare sidebar data for visualizing the database schema objects.

    Args:
        database_schema_dict (dict): A dictionary containing the database schema information.

    Returns:
        dict: A dictionary representing the sidebar data, organized by schema and table names.

    """
    logger.debug(f"Entering prepare_sidebar_data with database_schema_dict: {database_schema_dict}")
    sidebar_data = {}
    for table in database_schema_dict:
        schema_name = table["schema_name"]
        table_name = table["table_name"]
        columns = table["column_names"]

        if schema_name not in sidebar_data:
            sidebar_data[schema_name] = {}

        sidebar_data[schema_name][table_name] = columns
    logger.debug(f"Exiting prepare_sidebar_data with sidebar_data: {sidebar_data}")
    return sidebar_data
