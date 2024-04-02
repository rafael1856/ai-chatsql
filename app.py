import streamlit as st
from utils.config import db_credentials, MAX_TOKENS_ALLOWED, MAX_MESSAGES_TO_OPENAI, TOKEN_BUFFER
from utils.system_prompts import get_final_system_prompt
from utils.chat_functions import run_chat_sequence, clear_chat_history, count_tokens, prepare_sidebar_data
from utils.database_functions import database_schema_dict
from utils.function_calling_spec import functions
from utils.helper_functions import  save_conversation
from assets.dark_theme import dark
from assets.light_theme import light
from assets.made_by_sdw import made_by_sdw
import os
import markdown

def save_conversation_as_html(conversation):
    # print(conversation[0])  # print the first dictionary to see its keys
    conversation_str = '\n'.join([msg['content'] for msg in conversation])
    html_content = conversation_str #markdown.markdown(conversation_str)
    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Conversation</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    file_path = 'conversation_history/html_page.tml'
    with open(file_path, 'w') as f:
        f.write(html_page)
    return str(file_path)

def check_env_vars():
    vars = ['POSTGRES_SEMANTIC_DB', 'POSTGRES_USERNAME', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT']
    for var in vars:
        if var not in os.environ:
            print(f'Environment variable {var} is not set.')
            return False
    return True

def check_conda_env():
    if 'CONDA_DEFAULT_ENV' not in os.environ:
        print('No conda environment is currently active.')
        return False
    else:
        print(f'Current conda environment: {os.environ["CONDA_DEFAULT_ENV"]}')
        return True

if __name__ == "__main__":

# check precoditions to start the app
    # check if enviroment variables are set
    if not check_env_vars():
        print('Please set the environment variables before starting the app.')
        exit(1)
    if not check_conda_env():
        print('Please set the conda environment before starting the app.')
        exit(1)
      
    # check that the database is running

    ########### A. SIDEBAR ###########

    # Prepare data for the sidebar dropdowns
    sidebar_data = prepare_sidebar_data(database_schema_dict)
    st.sidebar.markdown("<div class='made_by'>Made by SDW🔋</div>", unsafe_allow_html=True)

    ### POSTGRES DB OBJECTS VIEWER ###

    st.markdown(made_by_sdw, unsafe_allow_html=True)
    st.sidebar.title("🔍 Postgres DB Objects Viewer")

    # Dropdown for schema selection
    selected_schema = st.sidebar.selectbox("📂 Select a schema", list(sidebar_data.keys()))

    # Dropdown for table selection based on chosen Schema
    selected_table = st.sidebar.selectbox("📜 Select a table", list(sidebar_data[selected_schema].keys()))

    # Display columns of the chosen table with interactivity using checkboxes
    st.sidebar.subheader(f"🔗 Columns in {selected_table}")
    for column in sidebar_data[selected_schema][selected_table]:
        is_checked = st.sidebar.checkbox(f"📌 {column}") 

    ### SAVE CONVERSATION BUTTON ###

    # Add a button to SAVE the chat/conversation
    if st.sidebar.button("Save Conversation MD"):
        saved_file_path = save_conversation(st.session_state["full_chat_history"])
        st.sidebar.success(f"Conversation saved to: {saved_file_path}")
        st.sidebar.markdown(f"Conversation saved! [Open File]({saved_file_path})")

    # Add a button to SAVE the chat/conversation
    if st.sidebar.button("Save Conversation HTML"):
        saved_file_path = save_conversation_as_html(st.session_state["full_chat_history"])
        st.sidebar.success(f"Conversation saved to: {saved_file_path}")
        st.sidebar.markdown(f"Conversation saved! [Open File]({saved_file_path})")

    ### CLEAR CONVERSATION BUTTON ###

    # Add a button to CLEAR the chat/conversation
    if st.sidebar.button("Clear Conversation🗑️"):
        save_conversation(st.session_state["full_chat_history"]) 
        clear_chat_history()

    ### TOGGLE THEME BUTTON ###

    # Retrieve the current theme from session state
    current_theme = st.session_state.get("theme", "light")
    st.markdown(f"<body class='{current_theme}'></body>", unsafe_allow_html=True)

    # Initialize the theme in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    # Add a button to toggle the UI colour theme
    if st.sidebar.button("Toggle Theme🚨"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

    # Apply the theme based on session state
    theme_style = dark if st.session_state.theme == "dark" else light
    st.markdown(theme_style, unsafe_allow_html=True)

    ########### B. CHAT INTERFACE ###########

    ### TITLE ###

    # Add title to the Streamlit chatbot app
    st.title("AI chat with a database")

    ### SESSION STATE ###

    # Initialize the full chat messages history for UI
    if "full_chat_history" not in st.session_state:
        st.session_state["full_chat_history"] = [{"role": "system", "content": get_final_system_prompt(db_credentials=db_credentials)}]

    # Initialize the API chat messages history for OpenAI requests
    if "api_chat_history" not in st.session_state:
        st.session_state["api_chat_history"] = [{"role": "system", "content": get_final_system_prompt(db_credentials=db_credentials)}]

    ### CHAT FACILITATION ###

    # Start the chat
    if (prompt := st.chat_input("What do you want to know?")) is not None:
        st.session_state.full_chat_history.append({"role": "user", "content": prompt})

        # Limit the number of messages sent to OpenAI by token count
        total_tokens = sum(count_tokens(message["content"]) for message in st.session_state["api_chat_history"])
        while total_tokens + count_tokens(prompt) + TOKEN_BUFFER > MAX_TOKENS_ALLOWED:
            removed_message = st.session_state["api_chat_history"].pop(0)
            total_tokens -= count_tokens(removed_message["content"])

        st.session_state.api_chat_history.append({"role": "user", "content": prompt})

    # Display previous chat messages from full_chat_history (ingore system prompt message)
    for message in st.session_state["full_chat_history"][1:]:
        if message["role"] == "user":
            st.chat_message("user", avatar='🧑‍💻').write(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant", avatar='🤖').write(message["content"])

    if st.session_state["api_chat_history"][-1]["role"] != "assistant":
        with st.spinner("⌛Connecting to AI model..."):
            # Send only the most recent messages to OpenAI from api_chat_history
            recent_messages = st.session_state["api_chat_history"][-MAX_MESSAGES_TO_OPENAI:]
            new_message = run_chat_sequence(recent_messages, functions)  # Get the latest message

            # Add this latest message to both api_chat_history and full_chat_history
            st.session_state["api_chat_history"].append(new_message)
            st.session_state["full_chat_history"].append(new_message)

            # Display the latest message from the assistant
            st.chat_message("assistant", avatar='🤖').write(new_message["content"])

        max_tokens = MAX_TOKENS_ALLOWED
        current_tokens = sum(count_tokens(message["content"]) for message in st.session_state["full_chat_history"])
        progress = min(1.0, max(0.0, current_tokens / max_tokens))
        st.progress(progress)
        st.write(f"Tokens Used: {current_tokens}/{max_tokens}")
        if current_tokens > max_tokens:
            st.warning("Note: Due to character limits, some older messages might not be considered in ongoing conversations with the AI.")
