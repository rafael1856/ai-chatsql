"""
database_functions.py

This module contains functions for interacting with a PostgreSQL database. 
It includes a function for getting the schema names in the database.

Imports:
    psycopg2: PostgreSQL database adapter for Python.
    config: Contains the database credentials.
    logger_config: Contains the function for configuring the logger.

Variables:
    logger: The logger configured from a JSON file.
    postgres_connection: The connection object to the PostgreSQL database.
    cursor: A database cursor to execute PostgreSQL commands.

Functions:
    get_schema_names(database_connection): Returns a list of schema names in the database.
    get_table_names(connection, schema_name): Returns a list of table names in the specified schema.
    get_column_names(connection, table_name, schema_name): Returns a list of column names in the specified table and schema.
    get_database_info(connection, schema_names): Fetches information about the schemas, tables, and columns in the database.
    ask_postgres_database(connection, query): Execute the SQL query provided and return the results.

The module establishes a connection with the PostgreSQL database using the credentials 
from the `config` module. If the connection is successful, it creates a database cursor 
for executing PostgreSQL commands. If the connection fails, it prints an error message 
and exits the program. The `get_schema_names` function takes a database connection object 
as a parameter and returns a list of schema names in the database.
"""

import sys
import psycopg2
from config import db_credentials
from logger_config import configure_logger_from_file

# Configure the logger based on the parameter file
logger = configure_logger_from_file('config.json')

# Establish connection with PostgreSQL
try:
    postgres_connection = psycopg2.connect(**db_credentials)
except psycopg2.OperationalError:
    print('Unable to connect to the database. Please make sure the database is running.')
    sys.exit()

postgres_connection.set_session(autocommit=True)
# Create a database cursor to execute PostgreSQL commands
cursor = postgres_connection.cursor()

# Validate the PostgreSQL connection status
if postgres_connection.closed == 0:
    print(f"Connected successfully to {db_credentials['dbname']} database\nConnection Details: {postgres_connection.dsn}")
else:
    raise ConnectionError("Unable to connect to the database")


def get_schema_names(database_connection):
    """Returns a list of schema names in the database.

    Args:
        database_connection: The connection object to the PostgreSQL database.

    Returns:
        A list of schema names.

    """
    logger.debug(f"Entering get_schema_names with database_connection: {database_connection}")

    cursor = database_connection.cursor()
    cursor.execute("SELECT schema_name FROM information_schema.schemata;")
    schema_names = [row[0] for row in cursor.fetchall()]
    cursor.close()

    logger.debug(f"Exiting get_schema_names with schema_names: {schema_names}")
    return schema_names

def get_table_names(connection, schema_name):
    """Returns a list of table names in the specified schema.

    Args:
        connection: The connection object to the PostgreSQL database.
        schema_name: The name of the schema.

    Returns:
        A list of table names.

    """
    logger.debug(f"Entering get_table_names with connection: {connection}, schema_name: {schema_name}")

    cursor = connection.cursor()
    cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
    table_names = [table[0] for table in cursor.fetchall()]
    cursor.close()
    logger.debug(f"Exiting get_table_names with table_names: {table_names}")
    return table_names

def get_column_names(connection, table_name, schema_name):
    """Returns a list of column names in the specified table and schema.

    Args:
        connection: The connection object to the PostgreSQL database.
        table_name: The name of the table.
        schema_name: The name of the schema.

    Returns:
        A list of column names.

    """
    logger.debug(f"Entering get_column_names with connection: {connection}, table_name: {table_name}, schema_name: {schema_name}")
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{schema_name}';")
    column_names = [col[0] for col in cursor.fetchall()]
    cursor.close()
    logger.debug(f"Exiting get_column_names with column_names: {column_names}")
    return column_names

def get_database_info(connection, schema_names):
    """Fetches information about the schemas, tables, and columns in the database.

    Args:
        connection: The connection object to the PostgreSQL database.
        schema_names: A list of schema names.

    Returns:
        A list of dictionaries containing information about each table, including the table name, column names, and schema name.

    """
    logger.debug(f"Entering get_database_info with connection: {connection}, schema_names: {schema_names}")
    table_dicts = []
    for schema in schema_names:
        for table_name in get_table_names(connection, schema):
            column_names = get_column_names(connection, table_name, schema)
            table_dicts.append({"table_name": table_name, "column_names": column_names, "schema_name": schema})
    logger.debug(f"Exiting get_database_info with table_dicts: {table_dicts}")
    return table_dicts

def ask_postgres_database(connection, query):
    """Execute the SQL query provided and return the results.

    Args:
        connection: The connection object to the PostgreSQL database.
        query: The SQL query to execute.

    Returns:
        The results of the query as a string, or an error message if the query fails.

    """
    logger.debug(f"Entering ask_postgres_database with connection: {connection}, query: {query}")
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = str(cursor.fetchall())
        cursor.close()
    except psycopg2.Error as error: # Catch a more specific exception
        results = f"Query failed with error: {error}"
    logger.debug(f"Exiting ask_postgres_database with results: {results}")
    return results

# To print details to the console:
# schemas = get_schema_names(postgres_connection)
# here you need to set schema name from postgres by default the schema is public in postgres database. you can see in pgadmin
schemas = ['listings']
database_schema_dict = get_database_info(postgres_connection, schemas)
database_schema_string = "\n".join(
    [
        f"Schema: {table['schema_name']}\nTable: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
        for table in database_schema_dict
    ]
)
