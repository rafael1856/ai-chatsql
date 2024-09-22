#!/bin/bash

# move to the docker app folder
cd /code/

# get enviroment variables
source .env

export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_PORT=8501

# clean old logs
rm /code/logs/*.log > /dev/null 2>&1

cd /code/src/
# Start the main app
streamlit run app.py --logger.level=debug



