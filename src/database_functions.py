"""
    TODO: add more error-handling 
    TODO: error-reporting and logging
    
"""
import psycopg2
from config import db_credentials

# Establish connection with PostgreSQL
try:
  postgres_connection = psycopg2.connect(**db_credentials)
except psycopg2.OperationalError:
  print(f"Unable to connect to the database using {postgres_connection}. Please make sure the database is running.")
  print(f"Connection Details: {postgres_connection.dsn}")  # DEBUG
  print(f"db_credentials : ' {db_credentials} '")  # DEBUG
  exit(1)

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
  cursor = database_connection.cursor()
  cursor.execute("SELECT schema_name FROM information_schema.schemata;")
  schema_names = [row[0] for row in cursor.fetchall()]
  cursor.close()
  return schema_names

def get_table_names(connection, schema_name):
  """Returns a list of table names in the specified schema.

  Args:
    connection: The connection object to the PostgreSQL database.
    schema_name: The name of the schema.

  Returns:
    A list of table names.

  """
  cursor = connection.cursor()
  cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
  table_names = [table[0] for table in cursor.fetchall()]
  cursor.close()
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
  cursor = connection.cursor()
  cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{schema_name}';")
  column_names = [col[0] for col in cursor.fetchall()]
  cursor.close()
  return column_names

def get_database_info(connection, schema_names):
  """Fetches information about the schemas, tables, and columns in the database.

  Args:
    connection: The connection object to the PostgreSQL database.
    schema_names: A list of schema names.

  Returns:
    A list of dictionaries containing information about each table, including the table name, column names, and schema name.

  """
  table_dicts = []
  for schema in schema_names:
    for table_name in get_table_names(connection, schema):
      column_names = get_column_names(connection, table_name, schema)
      table_dicts.append({"table_name": table_name, "column_names": column_names, "schema_name": schema})
      
  print(f"schema : ' {schema} '") # DEBUG
  print(f"schema_names : ' {schema_names} '") # DEBUG
  print(f"table_dicts : ' {table_dicts} '") # DEBUG
  return table_dicts

def ask_postgres_database(connection, query):
  """Execute the SQL query provided and return the results.

  Args:
    connection: The connection object to the PostgreSQL database.
    query: The SQL query to execute.

  Returns:
    The results of the query as a string, or an error message if the query fails.

  """
  try:
    cursor = connection.cursor()
    cursor.execute(query)
    results = str(cursor.fetchall())
    cursor.close()
  except Exception as e:
    results = f"Query failed with error: {e}"
  return results

# To print details to the console:
# schemas = get_schema_names(postgres_connection)
# here you need to set schema name from postgres by default the schema is public in postgres database. you can see in pgadmin
#schemas = ['employees']
schemas = ['employees']
database_schema_dict = get_database_info(postgres_connection, schemas)
database_schema_string = "\n".join(
    [
        f"Schema: {table['schema_name']}\nTable: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
        for table in database_schema_dict
    ]
)

print(f"database_schema_dict : ' {database_schema_dict} '") # DEBUG
print(f"database_schema_string : ' {database_schema_string} '") # DEBUG
