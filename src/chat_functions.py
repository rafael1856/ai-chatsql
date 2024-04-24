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

# import tiktoken
import streamlit as st
from config import AI_MODEL
from api_functions import send_api_request_to_openai_api, execute_function_call
from logger_config import configure_logger_from_file
import json
# from transformers import AutoTokenizer


# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

def run_chat_sequence(messages, functions):
    """
    Runs a chat sequence with the given messages and functions.

  Args:  messages (list):  Messages List exchanged in the chat sequence.
           functions (dict): A dictionary of available functions.
    Returns: dict: The last message in the chat history.
    Raises: KeyError: If the assistant message does not have a 'role' key.
    """
    logger.debug("At run_chat_sequence \n\n paramter messages: %s \n\n and parameter functions: %s", messages, functions)
    
    if "live_chat_history" not in st.session_state:
        st.session_state["live_chat_history"] = [{"role": "assistant", "content": "Hello! I'm Andy, how can I assist you?"}]
        # st.session_state["live_chat_history"] = []

    internal_chat_history = st.session_state["live_chat_history"].copy()

    chat_response = send_api_request_to_openai_api(messages, functions)
    assistant_message = chat_response.json()
    assistant_message_dict = json.loads(assistant_message)
    # Access the "content" value
    content_value = assistant_message_dict["content"]

    if assistant_message_dict["role"] == "assistant":
        internal_chat_history.append(assistant_message_dict)

    if assistant_message_dict.get("function_call"):
        results = execute_function_call(assistant_message_dict)
        internal_chat_history.append({"role": "function", "name": assistant_message_dict["function_call"]["name"], "content": results})

        internal_chat_history.append({"role": "user", "content": "You are a data analyst - provide personalized/customized explanations on what the results provided means and link them to the the context of the user query using clear, concise words in a user-friendly way. Or answer the question provided by the user in a helpful manner - either way, make sure your responses are human-like and relate to the initial user input. Your answers must not exceed 200 characters"})
        
        chat_response = send_api_request_to_openai_api(internal_chat_history, functions)
        assistant_message_dict = chat_response.json()["choices"][0]["message"]
        if assistant_message_dict["role"] == "assistant":
            st.session_state["live_chat_history"].append(assistant_message_dict)

    results = st.session_state["live_chat_history"][-1]
    logger.debug(f"Exiting run_chat_sequence with last message:{results}")
    return results

def clear_chat_history():
    """Clears the chat history stored in the Streamlit session state.

    This function removes the chat history stored in the Streamlit session state.
    It deletes the "live_chat_history", "full_chat_history", and "api_chat_history"
    variables from the session state.

    """
    del st.session_state["live_chat_history"]
    del st.session_state["full_chat_history"]
    del st.session_state["api_chat_history"]

    # Log the start and end of the clear_chat_history function
    logger.debug("clear_chat_history() just cleared live_chat, full_chat, and api_chat histories")

def count_tokens(response):
    # looking for token counting
    all_tokens = response.usage.json()
    # print(f"all_tokens used: {all_tokens} \n")

    all_tokens_dict = json.loads(all_tokens)
    # print(f"all_tokens_dict: {all_tokens_dict} \n")

    # Accessing the values for each key
    prompt_tokens = all_tokens_dict["prompt_tokens"]
    completion_tokens = all_tokens_dict["completion_tokens"]
    total_tokens = all_tokens_dict["total_tokens"]
    return total_tokens

# def count_tokens(text):
#     """
#     Count the total tokens used in a text string.
#     Args:
#         text (str): The input text string.
#     Returns:
#         int: The total number of tokens used in the text string.
#     """
#     logger.debug(f"Entering count_tokens with text: {text}")

#     if not isinstance(text, str):
#         return 0
    
#    # Split the text into words (tokens)
#     tokens = text.split()

#     # Count the tokens
#     total_tokens_in_text_string = len(tokens)
#     logger.debug(f"Exiting count_tokens with total tokens: {total_tokens_in_text_string}")
#     return total_tokens_in_text_string

#     # This only works with OpenAI GPT-3 models
#     # encoding = tiktoken.encoding_for_model(AI_MODEL)
#     # total_tokens_in_text_string = len(encoding.encode(text))
#     # logger.debug(f"Exiting count_tokens with total tokens: {total_tokens_in_text_string}")
#     # return total_tokens_in_text_string

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
    logger.debug(f"Exiting prepare_sidebar_data returned sidebar_data: {sidebar_data}")
    return sidebar_data
