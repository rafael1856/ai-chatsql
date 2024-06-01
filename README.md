# AI Database Chatbot
This is a fork from https://github.com/sdw-online/ai-postgres-database-chatbot

This is an AI chatbot that is able to answer any question about the information stored in a relational database. The chatbot created is plugged into a Postgres database. 

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

- `data`: This directory contains data used by the application. The `employees.sql.gz` file is a compressed SQL file, likely containing data about employees.

- `logs`: This directory contains log files. The `app.log` file is a log file for the main application.

- `docs`: This directory contains documentation for the project. The `postgresql-setup.md` file likely contains instructions for setting up a PostgreSQL database for this project.

- `LICENSE`: This file contains the license for the project, which dictates how others can use and contribute to the project.

- [``README.md``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Frafael%2Fdev%2Fprojects%2Fai-chatsql%2FREADME.md%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/rafael/dev/projects/ai-chatsql/README.md"): This file usually contains information about the project, such as what it does, how to install it, and how to use it.

- `start.sh` and `start.bat`: These are shell and batch scripts, respectively. They are used to start the application, and the commands they contain will be executed when they are run.

- `utils`: This directory contains utility scripts that are used throughout the project. The names of the files suggest that they contain various functions for interacting with APIs (`api_functions.py`), handling chat functionality (`chat_functions.py`), configuring the application (`config.py` and `config.json`), interacting with a database (`database_functions.py`), calling functions (`function_calling_spec.py`), general helper functions (`helper_functions.py`), configuring logging (`logger_config.py`), and handling system prompts (`system_prompts.py`).

# Installation 

1. Clone this repository with 'git clone URL'
        git clone git@github.com:rafael1856/ai-chatsql.git
      
2. Install PostgreSQL (only first time)
        Read document about postgresql at 'docs' folder

3. Add your database credentials in the user enviroment.
    
    In linux bash create a file 'env-vars' in the up-folder for app.
    This file should not be at the app folder for security reasons:
    ```
      export POSTGRES_SEMANTIC_DB='employees'
      export POSTGRES_USERNAME='user_database'
      export POSTGRES_PASSWORD='pass_database'
      export POSTGRES_HOST='localhost'
      export POSTGRES_PORT='5432'
    ```

    In Windows, update your start.bat file with the corresponding values 
    for your database.

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

5. Setup conda enviroment
    Linux
        from bash terminal, in the app folder
        run: source ./setup_conda
    Windows
        from command terminal, in the app folder
        run: conda env create -f conda_config.yaml
        run: activate chatsql

# Running the SqlChatbot 
    First time will ask for authorization email to use streamlit. 
    The app will be open in your default web browser.

    Linux
    - run: chmod 755 ./start.sh (if it was not executable)
        ./start.sh
   
    Windows
    - Be sure you have all setting updated on start.bat and run start.bat

# How to use it

* Ask questions related to data stored in the database the chatbot is connected to
* Get answers - Enjoy the structured and dynamic answers the chatbot provides  
* Save conversations - Preserve conversations into a markdown file for your future use 

# Visual Code extensions
arpinfidel.chartographer-extra
bierner.markdown-preview-github-styles
coddx.coddx-alpha
cweijan.dbclient-jdbc
cweijan.vscode-postgresql-client2
mayank1513.trello-kanban-task-board

