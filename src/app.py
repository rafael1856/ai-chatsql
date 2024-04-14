"""
This is the main module for the Streamlit application.

The application provides an interface for users to interact with a Postgres database using natural language queries. The queries are processed by an AI model, which generates SQL queries to retrieve the requested data from the database.

Functions:
- check_env_vars: Checks if the required environment variables for the database connection are set.
- check_conda_env: Checks if a conda environment is active.

Imports:
- streamlit: The main library for creating the web application.
- utils.config: Contains configuration variables for the application.
- utils.system_prompts: Contains system prompts for the AI model.
- utils.chat_functions: Contains functions for managing the chat history and interacting with the AI model.
- utils.database_functions: Contains functions for interacting with the database.
- utils.function_calling_spec: Contains specifications for calling functions in the AI model.
- utils.helper_functions: Contains helper functions for the application.
- os: Used for interacting with the operating system.
- markdown: Used for converting markdown text to HTML.
"""
import os
import sys
import streamlit as st
from config import db_credentials, MAX_TOKENS_ALLOWED, MAX_MESSAGES_TO_OPENAI, TOKEN_BUFFER
from system_prompts import get_final_system_prompt
from chat_functions import run_chat_sequence, clear_chat_history, count_tokens, prepare_sidebar_data
from database_functions import database_schema_dict
from function_calling_spec import functions
from helper_functions import  save_conversation
from logger_config import configure_logger_from_file

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

def check_env_vars():
    """
    Checks if the required environment variables are set.

    Returns:
        bool: True if all environment variables are set, False otherwise.
    """
    varis = ['POSTGRES_SEMANTIC_DB', 'POSTGRES_USERNAME', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT']
    for var in varis:
        if var not in os.environ:
            print(f'Environment variable {var} is not set.')
            return False
    return True

def check_conda_env():
    """
    Checks if a conda environment is currently active.

    Returns:
        bool: True if a conda environment is active, False otherwise.
    """
    if 'CONDA_DEFAULT_ENV' not in os.environ:
        print('No conda environment is currently active.')
        return False
    else:
        print(f'Current conda environment: {os.environ["CONDA_DEFAULT_ENV"]}')
        return True

if __name__ == "__main__":

    if not check_env_vars():
        print('Please set the environment variables before starting the app.')
        sys.exit()
    if not check_conda_env():
        print('Please set the conda environment before starting the app.')
        sys.exit()
    sidebar_data = prepare_sidebar_data(database_schema_dict)

    st.sidebar.title("Postgres DB Objects Viewer")

    selected_schema = st.sidebar.selectbox("Select a schema", list(sidebar_data.keys()))

    selected_table = st.sidebar.selectbox("Select a table", list(sidebar_data[selected_schema].keys()))

    st.sidebar.subheader(f"Columns in {selected_table}")
    for column in sidebar_data[selected_schema][selected_table]:
        is_checked = st.sidebar.checkbox(f"{column}")

    if st.sidebar.button("Save Conversation MD"):
        saved_file_path = save_conversation(st.session_state["full_chat_history"])
        st.sidebar.success(f"Conversation saved to: {saved_file_path}")
        st.sidebar.markdown(f"Conversation saved! [Open File]({saved_file_path})")

    if st.sidebar.button("Clear Conversation"):
        save_conversation(st.session_state["full_chat_history"])
        clear_chat_history()

    st.title("AI chat with a database")

    if "full_chat_history" not in st.session_state:
        st.session_state["full_chat_history"] = [{"role": "system", "content": get_final_system_prompt(db_credentials=db_credentials)}]

    if "api_chat_history" not in st.session_state:
        st.session_state["api_chat_history"] = [{"role": "system", "content": get_final_system_prompt(db_credentials=db_credentials)}]

    if (prompt := st.chat_input("What do you want to know?")) is not None:
        st.session_state.full_chat_history.append({"role": "user", "content": prompt})

        total_tokens = sum(count_tokens(message["content"]) for message in st.session_state["api_chat_history"])
        while total_tokens + count_tokens(prompt) + TOKEN_BUFFER > MAX_TOKENS_ALLOWED:
            removed_message = st.session_state["api_chat_history"].pop(0)
            total_tokens -= count_tokens(removed_message["content"])

        st.session_state.api_chat_history.append({"role": "user", "content": prompt})

    for message in st.session_state["full_chat_history"][1:]:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])

    if st.session_state["api_chat_history"][-1]["role"] != "assistant":
        with st.spinner("Connecting to AI model..."):
            recent_messages = st.session_state["api_chat_history"][-MAX_MESSAGES_TO_OPENAI:]
            new_message = run_chat_sequence(recent_messages, functions)

            st.session_state["api_chat_history"].append(new_message)
            st.session_state["full_chat_history"].append(new_message)

            st.chat_message("assistant").write(new_message["content"])

        # max_tokens = MAX_TOKENS_ALLOWED
        current_tokens = sum(count_tokens(message["content"]) for message in st.session_state["full_chat_history"])
        progress = min(1.0, max(0.0, current_tokens / MAX_TOKENS_ALLOWED))
        st.progress(progress)
        st.write(f"Tokens Used: {current_tokens}/{MAX_TOKENS_ALLOWED}")
        if current_tokens > MAX_TOKENS_ALLOWED:
            st.warning("Note: Due to character limits, some older messages might not be considered \
                       in ongoing conversations with the AI.")
