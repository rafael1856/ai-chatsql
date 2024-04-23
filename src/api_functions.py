"""
This module contains functions for interacting with the OpenAI API.

Functions:
- send_api_request_to_openai_api: Sends a request to the OpenAI API's chat completions endpoint. This function is decorated with a retry mechanism that waits for a random exponential time between attempts and stops after 3 attempts.
- execute_function_call: Executes a function call provided by the OpenAI API's response.

Imports:
- json: Used for handling JSON data.
- requests: Used for sending HTTP requests.
- utils.config: Contains configuration variables for the application.
- utils.database_functions: Contains functions for interacting with the database.
- tenacity: Provides a decorator for adding retry behavior to functions.

Exceptions:
- ConnectionError: Raised when a request to the OpenAI API fails.
"""

#
#TODO: THIS IS THE REFACTORED VERSION OF THE ORIGINAL CODE THAT USED REQUESTS.GET() directly.
#TODO: EXPLAIN THE CHANGES MADE AND WHY THEY WERE MADE.

#TODO: use this Phind Debug information
#The RetryError you're encountering indicates that the send_api_request_to_openai_api function, which is decorated
#with a retry mechanism using tenacity, has failed to execute successfully after the specified number of retry attempts.
#This could be due to several reasons, such as network issues, incorrect API credentials, or the API endpoint being unavailable.
# Here are steps to troubleshoot and potentially resolve this issue:
# Verify API Credentials and Endpoint: Ensure that the LM_STUDIO_API_KEY and the API endpoint URL (http://localhost:1234/v1) are correct. If you're running the LMStudio server locally, make sure it's up and running.
#Check Network Connectivity: If the LMStudio server is running on a different machine or a container, ensure that your
# machine can reach it. You can test this by pinging the server's IP address or using a tool like curl to make a
#request to the API endpoint.
#Review Retry Parameters: The retry mechanism is configured with wait_random_exponential(min=1, max=40) and
#stop_after_attempt(3). This means it will wait a random amount of time between 1 and 40 seconds between retries
# and will stop after 3 attempts. You might want to adjust these parameters based on your specific needs and environment.
# Inspect the Exception: Modify the send_api_request_to_openai_api function to print or log the exception that caused the retry mechanism to fail. This can provide more insight into what's going wrong.
#

import json
# import openai
from openai import OpenAI, ChatCompletion
from config import LM_STUDIO_API_KEY, AI_MODEL
# import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from database_functions import ask_postgres_database, postgres_connection
from logger_config import configure_logger_from_file
# from config import OPENAI_API_KEY, AI_MODEL

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')
# Initialize the OpenAI client with the local server URL and API key

# openai = OpenAI(base_url="http://localhost:9193/v1", api_key=LM_STUDIO_API_KEY)
client = OpenAI(base_url="http://localhost:9193/v1", api_key=LM_STUDIO_API_KEY)

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))

def send_api_request_to_openai_api(messages, functions=None, function_call=None, model=AI_MODEL, openai_api_key=LM_STUDIO_API_KEY):
    """
    Send the API request to the LMStudio API via Chat Completions endpoint.
    # Function prepares request_data object with all parameters needed for the API request.
    # Parameters include the model, messages, functions, and function_call parameters.

    Args:
        messages (list): A list of message objects containing 'role' and 'content' keys.
        functions (list, optional): A list of function objects. Defaults to None.
        function_call (dict, optional): A dictionary representing the function call. Defaults to None.
        model (str, optional): The model to use for the API request. Defaults to AI_MODEL.
        # openai_api_key (str, optional): The API key for the OpenAI API. Defaults to OPENAI_API_KEY.

    Returns: dict: The response object from the API request.
    Raises:  ConnectionError: If there is a failure to connect to the LMStudio API.
    """
    logger.debug(f"Entering send_api_request_to_openai_api with messages: {messages}, functions: {functions}, \
                 function_call: {function_call}, model: {model}, openai_api_key: {openai_api_key}")

    try:
        # Prepare the request_data object with all parameters needed for the API request
        # The function is called with the model, messages, functions, and function_call parameters
        request_data = {
            "model": model,
            "messages": messages, 
            # messages=history,
            # temperature : 0.7,
            # stream : True,
            # #"functions": functions,            # RSL added comment to clarity structur of request_data.
            # #"function_call": function_call 
        }
        if functions: 
            request_data.update({"functions": functions})
        if function_call: 
            request_data.update({"function_call": function_call})

        logger.info(f"Actual request_data: {request_data} sent to LMStudio API \n")
        
        # Send the request using the OpenAI client

        response = client.chat.completions.create(**request_data)

        # LM-Studio API call using OpenAI client
        #   completion = client.chat.completions.create(
        #   model="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/Hermes-2-Pro-Mistral-7B.Q4_0.gguf",
        #   messages=[
        #     {"role": "system", "content": "Always answer in rhymes."},
        #     {"role": "user", "content": "Introduce yourself."}
        #   ],
        #   temperature=0.7,
        # )


        # looking for token counting
        all_tokens = response.usage.json()
        print(f"all_tokens used: {all_tokens} \n")
        
        all_tokens = json.loads(response.usage)

        # Accessing the values for each key
        prompt_tokens = all_tokens["usage"]["prompt_tokens"]
        completion_tokens = all_tokens["usage"]["completion_tokens"]
        total_tokens = all_tokens["usage"]["total_tokens"]


        # Printing the values
        print(f"Prompt Tokens: {prompt_tokens}")
        print(f"Completion Tokens: {completion_tokens}")
        print(f"Total Tokens: {total_tokens}")

        
        logger.debug(f"\n\n Response: {response.choices[0].message} received from LMStudio API")
        return response.choices[0].message

    except Exception as e:
        print(f"Error in send_api_request_to_openai_api: {e}")
        raise ConnectionError(f"Failed to connect to LMStudio API due to: {e}")

def execute_function_call(message):
    """
    Run the function call provided by LMStudio's API response.
    Args:  message (dict): The API response message containing the function call details.
    Returns:  str: The results of the function call.
    Raises:
        None
    """
    logger.debug(f"Entering execute_function_call with message: {message}")
    if message["function_call"]["name"] == "ask_postgres_database":
        query = json.loads(message["function_call"]["arguments"])["query"]
        print(f"SQL query: {query} \n")     
        logger.info(f"SQL query: {query}")
        # TODO: These SQL statments should be saved for reuse.

        results = ask_postgres_database(postgres_connection, query)
        print(f"Results A: {results} \n")   
        logger.info(f"Results A: {results}")
        # TODO: These query results should be saved in a report.
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
        logger.debug(f"Entering execute_function_callreturned results: {results}")
    return results
