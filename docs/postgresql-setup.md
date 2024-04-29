# How to setup postrges in Linux Ubuntu 
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-22-04

run: sudo apt install postgresql postgresql-contrib

# Other tools / interfaces
install phppgAdmin
phppgadmin then go via browser to http://localhost/phppgadmin/ 

# Install sample database 
A dataset containing details about employees, their departments, salaries, and more.

# Create the database and schema:
  $ sudo -i -u postgres
  $ psql
    CREATE DATABASE employees;
    \c employees
    CREATE SCHEMA employees;

# Navigate to the directory data
The user/pass are the ones defined during postgres instalation

pg_restore -d postgres://<user>:<password>@<hostname>/employees -Fc employees.sql.gz -c -v --no-owner --no-privileges; 

Database objects are created in the employees schema rather than the public schema.

# Connect to the employees database:

psql postgres://<user>:<password>@<hostname>/employees

or 
```
  $ sudo -i -u postgres
    postgres@black217:~$ psql
    postgres-# \list
    postgres-# \c employees 
    You are now connected to database "employees" as user "postgres".
```
# How to see db information
employees-# \conninfo
You are connected to database "employees" as user "postgres" via socket in "/var/run/postgresql" at port "5432".

# How to give permissions
--- this was not enough to run queries...asked for SCHEMA permits ---
  ```
  $ sudo -i -u postgres
    $ psql
    postgres-# \list
    postgres-# \c employees 
    You are now connected to database "employees" as user "postgres".
    employees-# GRANT ALL PRIVILEGES ON DATABASE employees TO rafael;
  ```

# How to make a user super-user:
```
postgres-# ALTER USER myuser WITH SUPERUSER;
postgres-# \dp
```



# Setup PostgreSQL for Windows

-download version for Windows x86-64
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

go to download folder and start installation
- accept all default setup
- add postgres password and write it down
- continue installing stack builder
  - select postgres
  - postgreSQL...it is the local server
  - select in add-ons 'pgAgent', and next
    - pgAgent service account postgres / same password before 
      -  verify installation, go to windows menu and find pgAdmin 
 -  start pgAdmin (authorize it)


# Setup Employees Database
extract the compressed database employees.tar.gz into a tar file
right click with file explorer over employees.tar.gz, select extract all 

# Open pgAdmin app

right click on Databases/create database 
database name: employees and save

right click on employees/restore
- Format: Custom or tar
- Filename: select your employees.tar file (navegate to the app fodler /data/extracted )
- click restore

- restore messages 'process started' and 'process completed'
- verify: click on 'tables; and should see all tables and data
- right click on a table and select view/edit data

Here are more details about how to install postgres on Windows
https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/
