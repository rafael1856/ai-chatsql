#!/bin/bash
# This script is used to start the SQLChat application.

# clean old logs
rm logs/*.log
# Start the SQLChat application using Streamlit
streamlit run src/app.py