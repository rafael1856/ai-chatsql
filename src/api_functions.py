"""
TODO: THIS IS THE REFACTORED VERSION OF THE ORIGINAL CODE THAT USED REQUESTS.GET() directly. 
TODO: EXPLAIN THE CHANGES MADE AND WHY THEY WERE MADE.

TODO: use this Phind Debug information 
The RetryError you're encountering indicates that the send_api_request_to_openai_api function, which is decorated with a retry mechanism using tenacity, has failed to execute successfully after the specified number of retry attempts. This could be due to several reasons, such as network issues, incorrect API credentials, or the API endpoint being unavailable.

Here are steps to troubleshoot and potentially resolve this issue:

Verify API Credentials and Endpoint: Ensure that the LM_STUDIO_API_KEY and the API endpoint URL (http://localhost:1234/v1) are correct. If you're running the LMStudio server locally, make sure it's up and running.
Check Network Connectivity: If the LMStudio server is running on a different machine or a container, ensure that your machine can reach it. You can test this by pinging the server's IP address or using a tool like curl to make a request to the API endpoint.
Review Retry Parameters: The retry mechanism is configured with wait_random_exponential(min=1, max=40) and stop_after_attempt(3). This means it will wait a random amount of time between 1 and 40 seconds between retries and will stop after 3 attempts. You might want to adjust these parameters based on your specific needs and environment.
Inspect the Exception: Modify the send_api_request_to_openai_api function to print or log the exception that caused the retry mechanism to fail. This can provide more insight into what's going wrong.
##########################################################

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

import json
from openai import OpenAI, ChatCompletion
from config import LM_STUDIO_API_KEY, AI_MODEL
from database_functions import ask_postgres_database, postgres_connection
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Initialize the OpenAI client with the local server URL and API key
openai = OpenAI(base_url="http://localhost:1234/v1", api_key=LM_STUDIO_API_KEY)

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def send_api_request_to_openai_api(messages, functions=None, function_call=None, model=AI_MODEL):
    """
    Send the API request to the LMStudio API via Chat Completions endpoint.
    # This function prepares the request_data object with all parameters needed for the API request.
    # The parameters include the model, messages, functions, and function_call parameters.

    Args:
        messages (list): A list of message objects containing 'role' and 'content' keys.
        functions (list, optional): A list of function objects. Defaults to None.
        function_call (dict, optional): A dictionary representing the function call. Defaults to None.
        model (str, optional): The model to use for the API request. Defaults to AI_MODEL.

    Returns:
        dict: The response object from the API request.

    Raises:
        ConnectionError: If there is a failure to connect to the LMStudio API.
    """
    try:
        # Prepare the request_data object with all parameters needed for the API request
        # The function is called with the model, messages, functions, and function_call parameters
        request_data = {
            "model": model,
            "messages": messages, 
            #"functions": functions,
            #"function_call": function_call
        }
        if functions: 
            request_data.update({"functions": functions})
        if function_call: 
            request_data.update({"function_call": function_call})

        # Send the request using the OpenAI client
        response = openai.ChatCompletion.create(**request_data)

        return response

    except Exception as e:
        print(f"Error in send_api_request_to_openai_api: {e}")
        raise ConnectionError(f"Failed to connect to LMStudio API due to: {e}")

def execute_function_call(message):
    """
    Run the function call provided by LMStudio's API response.

    Args:
        message (dict): The API response message containing the function call details.

    Returns:
        str: The results of the function call.

    Raises:
        None
    """
    if message["function_call"]["name"] == "ask_postgres_database":
        query = json.loads(message["function_call"]["arguments"])["query"]
        print(f"SQL query: {query} \n")
        results = ask_postgres_database(postgres_connection, query)
        print(f"Results A: {results} \n")
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results