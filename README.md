# AI Database Chatbot
This is a fork from https://github.com/sdw-online/ai-postgres-database-chatbot

This is an AI chatbot that is able to answer any question about the information stored in a relational database. The chatbot created is plugged into a Postgres database. Additionally this version runs on a Docker container. Also postgress and pgadmin running on Docker.


# Tools 

* **Streamlit:** For an interactive, user-friendly web-based interface.
* **OpenAI:** The power behind the chatbot's intelligent responses.
* **Postgres:** The database where all the magic data resides.

# Folder Structure 
```
├── bin
    ├── app-setup-docker-program.sh
    ├── app-start-docker-program.sh
    ├── build-docker-images.sh
    ├── ollallm-setup-docker.sh
    ├── ollallm-start-docker-programs.sh
    ├── setup-conda.sh
    ├── start-docker-app.sh
    ├── start-docker-ollallm.sh
    ├── start-docker-postgres.sh
    └── start.sh
├── src
    ├── api_functions.py
    ├── app.py
    ├── chat_functions.py
    ├── config.json
    ├── config.py
    ├── database_functions.py
    ├── function_calling_spec.py
    ├── helper_functions.py
    ├── logger_config.py
├── conf
    ├── conda_config.yaml
    └── config
├── conversation_history
│   └── ....
├── data
│   └── employees.sql.gz
├── logs
│   └── app.log
├── docs
│   └── postgresql-setup.md
├── LICENSE
├── README.md

```

The active selection is a tree-like representation of the directory structure of a software project. Here's a brief explanation of what each file and directory might be used for:

- `app.py`: This is likely the main application file. When you run the application, this is the file that gets executed.

- `conda_config.yaml`: This file is used to configure a Conda environment. Conda is a package manager that helps you manage dependencies in your Python projects.

- `conversation_history`: This directory might contain logs or records of past conversations if this is a chatbot or similar application.

- `data`: This directory contains sample data used by the application. 
    Clean_db.sql, realestatedb.sql and fill_db.sql are sql script to create and fillup RealEsateDB.
    The `employees.sql.gz` file is a compressed SQL file, likely containing data about employees.
    Realestatedata.txt and zillow-data.txt are text files containing data about real estate.

- `logs`: This directory contains log files. The `app.log` file is a log file for the main application.

- `docs`: This directory contains documentation for the project. The `postgresql-setup.md` file likely contains instructions for setting up a PostgreSQL database for this project.

- `LICENSE`: This file contains the license for the project, which dictates how others can use and contribute to the project.

- [``README.md``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Frafael%2Fdev%2Fprojects%2Fai-chatsql%2FREADME.md%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/rafael/dev/projects/ai-chatsql/README.md"): This file usually contains information about the project, such as what it does, how to install it, and how to use it.

- `start.sh` other script on bin folder are shell and batch scripts. They are used to start the application, or the docker containers and the commands they contain will be executed when they are run.

# Installation locally

1. Clone this repository with 'git clone URL'
        git clone git@github.com:rafael1856/ai-chatsql.git
      
2. Install Docker (only first time)
        [Read documentation about Docker installation]](https://docs.docker.com/engine/install/) 


3. Add your configuraton file conf/config::
     # Set config values
        # system
        export DATA_FOLDER="data/"
        export LOG_FILE="logs/app.log"
        export SCHEMA="listing"
        export LOG_LEVEL="ERROR"
        export STREAMLIT_SERVER_ADDRESS=0.0.0.0
        export STREAMLIT_SERVER_PORT=8501
        export APPDIR="/home/nonroot/code"
        export MNTDIR="/code"

        # for postgres and pgadmin
        export POSTGRES_DB="realestate24"
        export POSTGRES_USER="myuser"
        export POSTGRES_PASSWORD="mypassword"
        export PGADMIN_DEFAULT_EMAIL="admin@example.com"
        export PGADMIN_DEFAULT_PASSWORD="adminpassword"
        export POSTGRES_HOST="pgvectordb1"
        export POSTGRES_PORT="5432"

        # for ollama and litellm
        export OLLAMA_HOST="0.0.0.0:11434"
        export MODEL="llama3.1"
        export OLLAMA_KEEP_ALIVE=24h
            
        # TODO: explain the following
        export UID="$(id -u)"
        export GID="$(id -g)"
            
        export OPENAI_API_KEY="sk-p0ouHvojFbzx8nBhusfsdfdsf"
   
4. Build images
    run: build-docker-images.sh
    results:
        ``` 
        - verifiy the images running: docker image ls
        
        ai-chatsql-ollallm (~ 10Gb)
        ankane/pgvector (~ 0.5Gb)
        dpage/pgadmin4  (~ 0.5Gb)
        condaforge/miniforge3:latest (~ 0.5Gb)
        
        - verify the containers created running: docker ps

        ollallm1
        pgvector1
        pgadmin1
        mamba1

        - And it should get these port mappings:

        ollallm1
        0.0.0.0:24000->4000/tcp, [::]:24000->4000/tcp, 0.0.0.0:21434->11434/tcp, [::]:21434->11434/tcp   

        pgvector1
        0.0.0.0:5432->5432/tcp, :::5432->5432/tcp                                                        

        pgadmin1
        443/tcp, 0.0.0.0:20080->80/tcp, [::]:20080->80/tcp                                               

        mamba1
        0.0.0.0:8501->8501/tcp, :::8501->8501/tcp                                                        
        ```

        Is status of the containers: is NOT up and running. Run:
        1) for start ollama + litellm: start-docker-ollallm.sh
        2) for start pgadmin and postgres: start-docker-postgres.sh
        3) for start ai-chatsql: start-docker-app.sh


# Running the SqlChatbot web interface
    browser: http://localhost:8501

# Running pgadmin web interface
    browser: http://localhost:20080

# How to use it

* Ask questions related to data stored in the database the chatbot is connected to
* Get answers - Enjoy the structured and dynamic answers the chatbot provides  
* Save conversations - Preserve conversations into a markdown file for your future use