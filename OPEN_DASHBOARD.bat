@echo off
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Opening SAMI Dashboard...
start http://localhost:8502
