@echo off
echo Starting Local Development Server...
call venv\Scripts\activate
uvicorn src.presentation.api.main:app --reload --env-file .env
pause
