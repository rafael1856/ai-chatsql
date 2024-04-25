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

from openai import OpenAI
import json
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from database_functions import ask_postgres_database, postgres_connection
from logger_config import configure_logger_from_file
from config import OPENAI_API_KEY, AI_MODEL

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))


def send_api_request_to_openai_api(messages1, functions=None, function_call=None, model=AI_MODEL, openai_api_key=OPENAI_API_KEY):
    """
    Send the API request to the OpenAI API via Chat Completions endpoint.

    Args:
        messages (list): A list of message objects containing 'role' and 'content' keys.
        functions (list, optional): A list of function objects. Defaults to None.
        function_call (dict, optional): A dictionary representing the function call. Defaults to None.
        model (str, optional): The model to use for the API request. Defaults to AI_MODEL.
        openai_api_key (str, optional): The API key for the OpenAI API. Defaults to OPENAI_API_KEY.

    Returns:
        requests.Response: The response object from the API request.

    Raises:
        ConnectionError: If there is a failure to connect to the OpenAI API.
    """
    logger.debug(f"Entering send_api_request_to_openai_api with messages: {messages1}, functions: {functions}, \
                 function_call: {function_call}, model: {model}, openai_api_key: {openai_api_key}")

    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai_api_key}"}
        json_data = {"model": model, "messages": messages1}

        logger.debug(f"model: {model}\n")
        print(f"messages: {messages1}\n")

# messages: [{'role': 'system', 'content': '\nYou are Andy, an AI PostgreSQL SQL specialist. Your mission is to decode user inquiries, create precise SQL scripts, run them, and succinctly display the results. Maintain Andy\'s persona throughout all communications.\n\nPlease adhere to these guidelines during interactions:\n<rules>\n1. Strictly use wildcards like "%keyword%" and the \'LIKE\' clause when trying to find text that might not match exactly.\n2. Ensure SQL variables don\'t start with numbers.\n3. Work with the given tables and columns, making no baseless assumptions.\n4. Generally, limit the amount of results to 10, unless otherwise noted.\n5. Present SQL queries in a neat markdown format, like ```sql code```.\n6. Aim to offer just a single SQL script in one response.\n7. Guard against SQL injection by cleaning user inputs.\n8. If a query doesn\'t yield results, suggest other possible avenues of inquiry.\n9. Prioritize user privacy; avoid retaining personal data.\n10. Strictly perform searches on tables in the {{schema}}.{{table}} format e.g. SELECT * FROM prod.dim_sales_agent_tbl WHERE seniority_level LIKE \'%enior%\' where prod = {{schema}} and dim_sales_agent_tbl = {{table}}\n</rules>\n\nBegin with a brief introduction as Andy and offer an overview of available metrics. However, avoid naming every table or schema. The introduction must not exceed 300 characters under any circumstance.\n\nFor each SQL output, include a brief rationale, display the outcome in the chat, and provide an explanation in context to the user\'s original request. Always format SQL as {{database}}.{{schema}}.{{table}}.\n\nBefore presenting, confirm the validity of SQL scripts and dataframes. Assess if a user\'s query truly needs a database response. If not, guide them as necessary.\n\n'}]


        if functions:
            json_data.update({"functions": functions})
        if function_call:
            json_data.update({"function_call": function_call})


        client = OpenAI(base_url="http://localhost:9193/v1", api_key="lm-studio")

        completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf",
        messages=[
            {"role": "system", "content": messages1[0]["content"]},
            {"role": "user", "content": "Introduce yourself."}
        ],
        temperature=0.7,
        )

        # print(completion.choices[0].message)
        response = completion #.choices[0].message
        # ["choices"][0]["message"]
       
        # logger.debug(f"response: {response}\n")
        print(f"\n\n response: {response}\n")
        return response
    

    except requests.RequestException as error:
        raise ConnectionError(f"Failed to connect to OpenAI API due to: {error}") from error

def execute_function_call(message):
    """
    Run the function call provided by OpenAI's API response.

    Args:
        message (dict): The API response message containing the function call details.

    Returns:
        str: The results of the function call.

    Raises:
        None

    """
    logger.debug(f"Entering execute_function_call with message: {message}")
    if message["function_call"]["name"] == "ask_postgres_database":
        query = json.loads(message["function_call"]["arguments"])["query"]
        # print(f"SQL query: {query} \n")
        logger.debug(f"SQL query: {query} \n")
        results = ask_postgres_database(postgres_connection, query)
        # print(f"Results A: {results} \n")
        logger.debug(f"Results A: {results} \n")
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results
