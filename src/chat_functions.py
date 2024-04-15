import tiktoken
import streamlit as st
from config import AI_MODEL
from api_functions import send_api_request_to_openai_api, execute_function_call

import logging
from datetime import datetime

# Configure logging
log_filename = f"app_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_chat_sequence(messages, functions):
    """
    Runs a chat sequence with the given messages and functions.

    Args:  messages (list):  Messages List exchanged in the chat sequence.
           functions (dict): A dictionary of available functions.
    Returns: dict: The last message in the chat history.
    Raises: KeyError: If the assistant message does not have a 'role' key.
    """

    # Log the start and end of the run_chat_sequence function
    logging.info("run_chat_sequence started with messages: %s and functions: %s", messages, functions)

    if "live_chat_history" not in st.session_state:
        st.session_state["live_chat_history"] = [{"role": "assistant", "content": "Hello! I'm Andy, how can I assist you?"}]
        # st.session_state["live_chat_history"] = []

    internal_chat_history = st.session_state["live_chat_history"].copy()

    chat_response = send_api_request_to_openai_api(messages, functions)
    assistant_message = chat_response.json()["choices"][0]["message"]
    
    if assistant_message["role"] == "assistant":
        internal_chat_history.append(assistant_message)

    if assistant_message.get("function_call"):

        results = execute_function_call(assistant_message)

        internal_chat_history.append({"role": "function", "name": assistant_message["function_call"]["name"], "content": results})

        internal_chat_history.append({"role": "user", "content": "You are a data analyst - provide personalized/customized explanations on what the results provided means and link them to the the context of the user query using clear, concise words in a user-friendly way.  Or answer the question provided by the user in a helpful manner - either way, make sure your responses are human-like and relate to the initial user input.  Your answers must not exceed 200 characters"})

        chat_response = send_api_request_to_openai_api(internal_chat_history, functions)
        
        assistant_message = chat_response.json()["choices"][0]["message"]
        if assistant_message["role"] == "assistant":
            st.session_state["live_chat_history"].append(assistant_message)

        logging.info("run_chat_sequence ended with result: %s", assistant_message)  # Log the result for debugging.

    return st.session_state["live_chat_history"][-1]

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
    logging.info("clear_chat_history() just cleared live_chat, full_chat, and api_chat histories")


def count_tokens(text):
    """Count the total tokens used in a text string.

    Args:
      text (str): The input text string.

    Returns:
      int: The total number of tokens used in the text string.
    """
    if not isinstance(text, str):  
      return 0 
    encoding = tiktoken.encoding_for_model(AI_MODEL)
    total_tokens_in_text_string = len(encoding.encode(text))
    
    return total_tokens_in_text_string

def prepare_sidebar_data(database_schema_dict):
    """ 
    Prepare sidebar data for visualizing the database schema objects.
    Args:  database_schema_dict (dict): Contain database schema information.
    Returns:  dict: Represents sidebar data, organized by schema and table names.
    """
    sidebar_data = {}
    
    for table in database_schema_dict:
        schema_name = table["schema_name"]
        table_name = table["table_name"]
        columns = table["column_names"]

        if schema_name not in sidebar_data:
            sidebar_data[schema_name] = {}

        sidebar_data[schema_name][table_name] = columns
        
        logging.info("prepare_sidebar_data() returned sidebar_data : {sidebar_data}.")
        
    return sidebar_data

