#!/bin/bash

# move to the docer app folder
cd /code/

# get enviroment variables
source .env

# clean old logs
rm logs/*.log > /dev/null 2>&1

# Start the main app
streamlit run src/app.py --logger.level=debug



