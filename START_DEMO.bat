@echo off
title SAMI Transfer Bot - LIVE DEMO
color 0A
echo.
echo ================================================
echo    SAMI TRANSFER BOT - LIVE DEMO MODE
echo ================================================
echo.
echo This will start BOTH the dashboard AND simulator!
echo.
echo Features:
echo  - Green "DEMO LIVE" indicator
echo  - Auto-refresh every 5 seconds
echo  - Simulated emails every 10 seconds
echo  - CRITICAL/urgent emails every 5th email
echo  - Perfect for demonstrations!
echo.
echo ================================================
echo.
echo [1/2] Starting Dashboard...

REM Start dashboard in a new window
if exist "venv\Scripts\python.exe" (
    start "SAMI Dashboard" cmd /c "venv\Scripts\python.exe -m streamlit run dashboard.py"
) else (
    start "SAMI Dashboard" cmd /c "python -m streamlit run dashboard.py"
)

timeout /t 3 /nobreak >nul

echo [2/2] Starting Demo Simulator...
echo.
echo ================================================
echo  Dashboard: http://localhost:8501
echo  Simulator: Running below
echo  Press Ctrl+C to stop the simulator
echo ================================================
echo.

REM Run simulator in this window
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe demo_simulator.py
) else (
    python demo_simulator.py
)

pause
