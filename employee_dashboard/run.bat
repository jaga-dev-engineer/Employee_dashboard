@echo off
REM Local-only dashboard access; employee data is not exposed to the network.
call venv\Scripts\activate
set LOCAL_ONLY_ACCESS=true
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
