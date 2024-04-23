"""
This module is used for setting up configuration variables for a program. 

It uses the os and dotenv modules to load environment variables from a .env file.

The module sets up the following:

1. Postgres database credentials: These are read from environment variables and stored in a dictionary.
2. OpenAI API key: This is read from an environment variable.
3. AI model: This is set to a specific model name.
4. Various configuration values related to the OpenAI API: These are set to specific numbers.

The purpose of this module is to set up the configuration for a program that interacts with a Postgres database and the OpenAI API.

Variables:
    db_credentials (dict): A dictionary that holds the credentials for a Postgres database.
    OPENAI_API_KEY (str): A variable that holds the API key for the OpenAI API.
    AI_MODEL (str): A variable that holds the name of the AI model to be used.
    MAX_TOKENS_ALLOWED (int): The maximum number of tokens permitted within a conversation exchange via the OpenAI API.
    MAX_MESSAGES_TO_OPENAI (int): The maximum number of messages to exchange with the OpenAI API.
    TOKEN_BUFFER (int): An arbitrary number to provide a buffer to avoid reaching exact token limits.
"""
import os
from dotenv import load_dotenv


load_dotenv()

# Set up Postgres database credentials
db_credentials = {
    'dbname'    :   os.getenv("POSTGRES_SEMANTIC_DB"),
    'user'      :   os.getenv("POSTGRES_USERNAME"),
    'password'  :   os.getenv("POSTGRES_PASSWORD"),
    'host'      :   os.getenv("POSTGRES_HOST"),
    'port'      :   os.getenv("POSTGRES_PORT")
}

# Set up OpenAI variables
# OPENAI_API_KEY  =   os.getenv("OPENAI_API_KEY")
# AI_MODEL        =   'gpt-3.5-turbo-16k'
# AI_MODEL        =   'gpt-4'

LM_STUDIO_API_KEY = "lm-studio"
# AI_MODEL = 'NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/Hermes-2-Pro-Mistral-7B.Q4_0.gguf'
AI_MODEL = 'TheBloke/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q2_K.gguf'

# Max number of tokens permitted within a conversation exchange via OpenAI API
MAX_TOKENS_ALLOWED      =   3000

# Max number of messages to exchange with OpenAI API
MAX_MESSAGES_TO_OPENAI  =   5

# An arbitrary number to provide a buffer to avoid reaching exact token limits
TOKEN_BUFFER            =   100

