# How to setup postrgess in Ubuntu 
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-22-04

run: sudo apt install postgresql postgresql-contrib

# How to setup password for defalut user postgres ?

# Other tools / interfaces
install phppgAdmin ?
phppgadmin then go via browser to http://localhost/phppgadmin/ 

pgAdmin GUI - no lo instale

# Install sample database 
https://github.com/neondatabase/postgres-sample-dbs

testing
https://github.com/neondatabase/postgres-sample-dbs?tab=readme-ov-file#employees-database

A dataset containing details about employees, their departments, salaries, and more.

# Create the database and schema:
    
  $ sudo -i -u postgres
  $ psql
    CREATE DATABASE employees;
    \c employees
    CREATE SCHEMA employees;

# Download the source file:
wget https://raw.githubusercontent.com/neondatabase/postgres-sample-dbs/main/employees.sql.gz
-or-
use the database file from data folder
cd data folder and run the code in the next step

# Navigate to the directory where you downloaded the source file, and run the following command:
The user/pass are the ones defined during postgres instalation

pg_restore -d postgres://<user>:<password>@<hostname>/employees -Fc employees.sql.gz -c -v --no-owner --no-privileges

pg_restore -d postgres://postgres:admin123@localhost/employees -Fc employees.sql.gz -c -v --no-owner --no-privileges

Database objects are created in the employees schema rather than the public schema.

# Connect to the employees database:

psql postgres://<user>:<password>@<hostname>/employees

psql postgres://postgres:admin123@localhost/employees


or 
```
  $ sudo -i -u postgres
    postgres@black217:~$ psql
    postgres-# \list
    postgres-# \c employees 
    You are now connected to database "employees" as user "postgres".
```
# How to add users?

# How to give just read/write permits ?

# How to see db information
employees-# \conninfo
You are connected to database "employees" as user "postgres" via socket in "/var/run/postgresql" at port "5432".

# How to give permissions
--- this was not enough to run queries...asked for SCHEMA permits ---
  ```
  $ sudo -i -u postgres
    postgres@black217:~$ psql
    postgres-# \list
    postgres-# \c employees 
    You are now connected to database "employees" as user "postgres".
    employees-# GRANT ALL PRIVILEGES ON DATABASE employees TO rafael;
    employees-# GRANT ALL PRIVILEGES ON DATABASE employees TO postgres;
  ```

# How to make a user super-user:
```
postgres-# ALTER USER myuser WITH SUPERUSER;
postgres-# \dp
```

postgres-# ALTER USER postgres WITH SUPERUSER;
postgres-# \dp