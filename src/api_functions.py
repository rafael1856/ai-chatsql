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

from openai import OpenAI
import json
import requests
from config import OPENAI_API_KEY, AI_MODEL
from database_functions import ask_postgres_database, postgres_connection
from tenacity import retry, wait_random_exponential, stop_after_attempt

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))


def send_api_request_to_openai_api(messages, functions=None, function_call=None, model=AI_MODEL, openai_api_key=OPENAI_API_KEY):
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
  try:

    # client = OpenAI(base_url="http://localhost:8083/v1", api_key="lm-studio")

    # completion = client.chat.completions.create(
    #   model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf",
    #   messages=[
    #     {"role": "system", "content": "Always answer like an infant of 8 years old."},
    #     {"role": "user", "content": "Tell me what do you want to play with me."},
    #   ],
    #   temperature=0.3,
    # )

    # print(completion.choices[0].message)


    # headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai_api_key}"}
    headers = {"Content-Type": "application/json", "Authorization": "lm-studio"}

    model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf",
    json_data = {"model": model, "messages": messages}

    if functions: 
      json_data.update({"functions": functions})

    if function_call: 
      json_data.update({"function_call": function_call})

    # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
    response = requests.post("http://localhost:8083/v1/chat/completions", headers=headers, json=json_data)


    response.raise_for_status()

    return response
  
  except requests.RequestException as e:
    raise ConnectionError(f"Failed to connect to OpenAI API due to: {e}")

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
  if message["function_call"]["name"] == "ask_postgres_database":
    query = json.loads(message["function_call"]["arguments"])["query"]
    print(f"SQL query: {query} \n")
    results = ask_postgres_database(postgres_connection, query)
    print(f"Results A: {results} \n")
  else:
    results = f"Error: function {message['function_call']['name']} does not exist"
  return results

