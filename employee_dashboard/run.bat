@echo off
REM Starts the dashboard on your network. Run setup first (see README.md).
call venv\Scripts\activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000
