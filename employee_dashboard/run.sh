#!/usr/bin/env bash
# Local-only dashboard access; employee data is not exposed to the network.
source venv/bin/activate
LOCAL_ONLY_ACCESS=true python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
