# AI Database Chatbot

This is an AI chatbot that is able to answer any question about the information stored in a relational database. The chatbot created is plugged into a Postgres database. 

# Tools 

* **Streamlit:** For an interactive, user-friendly web-based interface.
* **OpenAI:** The power behind the chatbot's intelligent responses.
* **Postgres:** The database where all the magic data resides.

# Folder Structure 

```

│   .env
│   .gitignore
│   app.py
│   README.md
│   requirements.txt
│
├───assets
│   │   dark_theme.py
│   │   light_theme.py
│   │   made_by_sdw.py
│   │
│   └───__pycache__
│           ...
│
├───conversation_history
│       ...
│
└───utils
    │   api_functions.py
    │   chat_functions.py
    │   config.py
    │   database_functions.py
    │   function_calling_spec.py
    │   helper_functions.py
    │   system_prompts.py
    │
    └───__pycache__
            ...

```

# Installation 

1. Clone this repository with 'git clone URL'
2. Run: conda env create -n sqlchat -f conda_config.yaml
3. Run: conda activate sqlchat
4. Install PostgreSQL
5. Add your database credentials in the user enviroment
    in Linux bash create a file 'env-vars' with:
      export POSTGRES_SEMANTIC_DB='employees'
      export POSTGRES_USERNAME='user_database'
      export POSTGRES_PASSWORD='pass_database'
      export POSTGRES_HOST='localhost'
      export POSTGRES_PORT='5432'
      and run: source ./env-vars

6. Add your OpenAI API key in the user enviroment
    in Linux bash, add to your .bashrc file:
      export OPENAI_API_KEY='your-api-key-value'
      then reload your .bashrc runnig source .bashrc

# Running the Chatbot 

```
streamlit run app.py
```

2. The chatbot UI will open in your default web browser. Engage and enjoy!

# How to use it

* Ask questions - Post questions related to data stored in the database the chatbot is connected to
* Get answers - Enjoy the structured and dynamic answers the chatbot provides  
* Save conversations - Preserve conversations into a markdown file for your future use 


