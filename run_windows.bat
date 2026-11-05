@echo off
title AffiliateFlow AI
if not exist .venv\Scripts\activate.bat (
  echo Please run setup_windows.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate
streamlit run app.py
pause
