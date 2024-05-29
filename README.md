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

# Installation 

1. Clone this repository with 'git clone URL'
      
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


