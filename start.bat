@echo off

rem Set environment variables
set "POSTGRES_SEMANTIC_DB=employees"
set "POSTGRES_USERNAME=postgres"
set "POSTGRES_PASSWORD=<pass-postgres>"
set "POSTGRES_HOST=localhost"
set "POSTGRES_PORT=5432"
set "OPENAI_API_KEY=<sk-...>"

rem delete old logs
del /q logs\*

rem Run the streamlit app
streamlit run src/app.py