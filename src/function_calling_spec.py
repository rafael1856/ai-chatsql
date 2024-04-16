"""
function_calling_spec.py

This module contains the specification for the `ask_postgres_database` function 
that is used to answer user questions about the database. The output of this 
function should be a fully formed SQL query.

Imports:
    database_functions: Contains the `database_schema_string` function.
    logger_config: Contains the function for configuring the logger.

Variables:
    logger: The logger configured from a JSON file.
    functions: A list of dictionaries that specify the function descriptions for 
    OpenAI function calling. Each dictionary contains the function name, description, 
    and parameters.

The `ask_postgres_database` function takes a single parameter, `query`, which is 
a string that represents the SQL query to extract information from the Postgres 
database. The SQL query should be written in the schema structure provided by 
`database_schema_string` and should not include any line breaks or characters 
that cannot be executed in Postgres.
"""

from database_functions import database_schema_string
from logger_config import configure_logger_from_file

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

# Specify function descriptions for OpenAI function calling
functions = [
    {
        "name": "ask_postgres_database",
        "description": "Use this function to answer user questions about the database. Output should be a fully formed SQL query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f""" The SQL query that extracts the information that answers the user's question from the Postgres database. Write the SQL in the following schema structure:
                            {database_schema_string}. Write the query in SQL format only, not in JSON. Do not include any line breaks or characters that cannot be executed in Postgres.  
                            """,
                }
            },
            "required": ["query"],
        },
    }
]
