@echo off
title AffiliateFlow AI - Setup
python --version
if errorlevel 1 (
  echo Python was not found. Install Python 3.11+ and tick Add Python to PATH.
  pause
  exit /b 1
)
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Setup complete. Edit .env and add your Gemini API key.
pause
