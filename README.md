# AI Database Chatbot
This is a fork from https://github.com/sdw-online/ai-postgres-database-chatbot

This is an AI chatbot that is able to answer any question about the information stored in a relational database. The chatbot created is plugged into a Postgres database. Additionally this version runs on a Docker container. Also postgress and pgadmin running on Docker.

# Tools 

* **Streamlit:** For an interactive, user-friendly web-based interface.
* **OpenAI:** The power behind the chatbot's intelligent responses.
* **Postgres:** The database where all the magic data resides.

# Folder Structure 
```
.
├── app.py
├── conda_config.yaml
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
├── start.sh
├── start.bat
└── utils
    ├── api_functions.py
    ├── chat_functions.py
    ├── config.py
    ├── config.json
    ├── database_functions.py
    ├── function_calling_spec.py
    ├── helper_functions.py
    ├── logger_config.py
    └── system_prompts.py
```

The active selection is a tree-like representation of the directory structure of a software project. Here's a brief explanation of what each file and directory might be used for:

- `app.py`: This is likely the main application file. When you run the application, this is the file that gets executed.

- `conda_config.yaml`: This file is used to configure a Conda environment. Conda is a package manager that helps you manage dependencies in your Python projects.

- `conversation_history`: This directory might contain logs or records of past conversations if this is a chatbot or similar application.

- `data`: This directory contains sample data used by the application. 
    Clean_db.sql, realstatedb.sql and fill_db.sql are sql script to create and fillup RealSateDB.
    The `employees.sql.gz` file is a compressed SQL file, likely containing data about employees.
    Realstatedata.txt and zillow-data.txt are text files containing data about real estate.

- `logs`: This directory contains log files. The `app.log` file is a log file for the main application.

- `docs`: This directory contains documentation for the project. The `postgresql-setup.md` file likely contains instructions for setting up a PostgreSQL database for this project.

- `LICENSE`: This file contains the license for the project, which dictates how others can use and contribute to the project.

- [``README.md``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Frafael%2Fdev%2Fprojects%2Fai-chatsql%2FREADME.md%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/rafael/dev/projects/ai-chatsql/README.md"): This file usually contains information about the project, such as what it does, how to install it, and how to use it.

- `start.sh` and `start.bat`: These are shell and batch scripts, respectively. They are used to start the application, and the commands they contain will be executed when they are run.

- `utils`: This directory contains utility scripts that are used throughout the project. The names of the files suggest that they contain various functions for interacting with APIs (`api_functions.py`), handling chat functionality (`chat_functions.py`), configuring the application (`config.py` and `config.json`), interacting with a database (`database_functions.py`), calling functions (`function_calling_spec.py`), general helper functions (`helper_functions.py`), configuring logging (`logger_config.py`), and handling system prompts (`system_prompts.py`).

# Installation locally

1. Clone this repository with 'git clone URL'
        git clone git@github.com:rafael1856/ai-chatsql.git
      
2. Install Docker (only first time)
        [Read document about](https://docs.docker.com/engine/install/) 


3. Add your database credentials in the .env file:
        # for postgres and pgadmin
        export POSTGRES_DB=realestate
        export POSTGRES_USER=myuser
        export POSTGRES_PASSWORD=mypassword
        export PGADMIN_DEFAULT_EMAIL=admin@example.com
        export PGADMIN_DEFAULT_PASSWORD=adminpassword

        export POSTGRES_HOST='pgvectordb1'
        export POSTGRES_PORT='5432'

        # for ollama and litellm
        export OLLAMA_HOST="127.0.0.1:11434"
        export OLLAMA_KEEP_ALIVE=24h
        export OLLAMA_DEBUG=1        

        # 
        export UID="$(id -u)"
        export GID="$(id -g)"
    
    In linux bash create a file 'env-vars' in the up-folder for app.
    This file should not be at the app folder for security reasons:
    ```
      export POSTGRES_SEMANTIC_DB='employees'
      export POSTGRES_USERNAME='user_database'
      export POSTGRES_PASSWORD='pass_database'
      export POSTGRES_HOST='localhost'
      export POSTGRES_PORT='5432'
    ```

4. Add your OpenAI API key in the user enviroment
    Linux bash, add to your .bashrc file:
    ```
      export OPENAI_API_KEY='your-api-key-value'
    ```
      then reload your .bashrc runnig source .bashrc (only first time)

    Windows modify your the start.bat file:
    ```
      set OPENAI_API_KEY='your-api-key-value'
    ```  

    
5. Build images
    run: build-docker-images.sh
    results:
        ``` 
        4 images created:
            verifiy the images running: docker image ls
        
        ai-chatsql-ollallm (~ 10Gb)
        ankane/pgvector (~ 0.5Gb)
        dpage/pgadmin4  (~ 0.5Gb)
        condaforge/miniforge3:latest (~ 0.5Gb)
        
        4 verify the containers created running: docker ps

        ollallm1
        pgvector1
        pgadmin1
        mamba1

        And it should get these port mappings:

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
        2) for start pgadmin and postgress: start-docker-postgres.sh
        3) for start ai-chatsql: start-docker-app.sh


# Running the SqlChatbot web interface
    browser: http://localhost:8501

# running pgadmin web interface
    browser: http://localhost:20080

# How to use it

* Ask questions related to data stored in the database the chatbot is connected to
* Get answers - Enjoy the structured and dynamic answers the chatbot provides  
* Save conversations - Preserve conversations into a markdown file for your future use