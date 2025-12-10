@echo off
title SAMI Transfer Bot - Update
color 0B
echo.
echo ============================================
echo     SAMI Transfer Bot - Update Manager
echo ============================================
echo.
echo Checking for updates from GitHub...
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

REM Pull latest changes
echo Downloading latest updates...
echo.
git pull origin main

if %ERRORLEVEL% EQU 0 (
    color 0A
    echo.
    echo ============================================
    echo     UPDATE COMPLETE!
    echo ============================================
    echo.
    echo Your bot is now up to date.
) else (
    color 0E
    echo.
    echo ============================================
    echo     UPDATE NOTICE
    echo ============================================
    echo.
    echo There may have been an issue with the update.
    echo If you see merge conflicts, contact Jason.
)

echo.
pause
