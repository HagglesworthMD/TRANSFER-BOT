@echo off
title SAMI Transfer Bot - Running
color 0A

echo.
echo ======================================
echo    SAMI TRANSFER BOT - STARTING
echo ======================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Bot is now monitoring emails...
echo Press Ctrl+C to stop
echo.

python distributor.py

pause
