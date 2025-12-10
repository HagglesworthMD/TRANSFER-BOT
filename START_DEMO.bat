@echo off
title SAMI Transfer Bot - DEMO MODE
color 0E
echo.
echo ========================================
echo    SAMI TRANSFER BOT - DEMO MODE
echo ========================================
echo.
echo Starting dashboard in DEMO MODE...
echo.
echo Features:
echo  - Yellow "DEMO MODE" indicator
echo  - No auto-refresh
echo  - Shows existing data
echo  - Safe for presentations
echo  - No email processing
echo.
echo Dashboard will open in your browser...
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

streamlit run dashboard.py

pause
