import psycopg2
from utils.config import db_credentials

# Establish connection with PostgreSQL
postgres_connection = psycopg2.connect(**db_credentials)
postgres_connection.set_session(autocommit=True)

# Create a database cursor to execute PostgreSQL commands
cursor = postgres_connection.cursor()

# Validate the PostgreSQL connection status
if postgres_connection.closed == 0:
    print(f"Connected successfully to {db_credentials['dbname']} database\nConnection Details: {postgres_connection.dsn}")
else:
    raise ConnectionError("Unable to connect to the database")

def get_schema_names(database_connection):
  """ Returns a list of schema names """
  cursor = database_connection.cursor()
  cursor.execute("SELECT schema_name FROM information_schema.schemata;")
  schema_names = [row[0] for row in cursor.fetchall()]
  cursor.close()
  return schema_names

# def get_schemas(db_credentials):
#     try:
#         # Establish a connection to the database
#         conn = psycopg2.connect(**db_credentials)

#         # Create a new cursor object
#         cur = conn.cursor()

#         # Execute a query to get all schema names
#         cur.execute("SELECT schema_name FROM information_schema.schemata")

#         # Fetch all the rows
#         rows = cur.fetchall()

#         # Close the cursor and connection
#         cur.close()
#         conn.close()

#         # Extract the schema names and return them
#         return [row[0] for row in rows]
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []
    
def get_table_names(connection, schema_name):
  """ Returns a list of table names """
  cursor = connection.cursor()
  cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
  table_names = [table[0] for table in cursor.fetchall()]
  cursor.close()
  return table_names

def get_column_names(connection, table_name, schema_name):
    """ Returns a list of column names """
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{schema_name}';")
    column_names = [col[0] for col in cursor.fetchall()]
    cursor.close()
    return column_names

def get_database_info(connection, schema_names):
    """ Fetches information about the schemas, tables and columns in the database """
    table_dicts = []
    for schema in schema_names:
        for table_name in get_table_names(connection, schema):
            column_names = get_column_names(connection, table_name, schema)
            table_dicts.append({"table_name": table_name, "column_names": column_names, "schema_name": schema})
    print("get_database_info ====", table_dicts)
    return table_dicts

# To print details to the console:
# schemas = get_schema_names(postgres_connection)
# here you need to set schema name from postgres by default the schema is public in postgres database. you can see in pgadmin
schemas = ['employees']
database_schema_dict = get_database_info(postgres_connection, schemas)
database_schema_string = "\n".join(
    [
        f"Schema: {table['schema_name']}\nTable: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
        for table in database_schema_dict
    ]
)

def ask_postgres_database(connection, query):
    """ Execute the SQL query provided by OpenAI and return the results """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = str(cursor.fetchall())
        cursor.close()
    except Exception as e:
        results = f"Query failed with error: {e}"
    return results