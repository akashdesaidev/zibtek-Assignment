@echo off
echo Starting Zibtek Backend with UV...
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

