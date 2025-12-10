@echo off
title SAMI Transfer Bot - Complete System
color 0B

echo.
echo ================================================
echo    SAMI TRANSFER BOT - STARTING ALL SYSTEMS
echo ================================================
echo.
echo [1/2] Opening Dashboard in browser...
start http://localhost:8502
timeout /t 2 /nobreak >nul

echo [2/2] Starting Email Bot...
echo.
echo ------------------------------------------------
echo Bot is now running - monitoring emails
echo Dashboard: http://localhost:8502
echo Press Ctrl+C to stop the bot
echo ------------------------------------------------
echo.

venv\Scripts\python.exe distributor.py

pause
