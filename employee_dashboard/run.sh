#!/usr/bin/env bash
# Starts the dashboard on your network. Run setup first (see README.md).
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000
