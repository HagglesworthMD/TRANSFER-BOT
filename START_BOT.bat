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

venv\Scripts\python.exe distributor.py

pause
