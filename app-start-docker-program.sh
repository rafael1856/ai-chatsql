#!/bin/bash

# get enviroment variables
source .env

# move to the docer app folder
cd /code/

# clean old logs
rm logs/*.log > /dev/null 2>&1

# Start the main app
streamlit run src/app.py



