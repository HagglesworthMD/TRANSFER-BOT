@echo off
title SAMI Transfer Bot - Running
color 0A

echo.
echo ======================================
echo    SAMI TRANSFER BOT - STARTING
echo ======================================
echo.
echo Bot is now monitoring emails...
echo Press Ctrl+C to stop
echo.

REM Try venv first, fall back to system Python
if exist "venv\Scripts\python.exe" (
    echo Using virtual environment...
    venv\Scripts\python.exe distributor.py
) else (
    echo Using system Python...
    python distributor.py
)

pause
