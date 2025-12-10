@echo off
title Installing SAMI Transfer Bot Dependencies
color 0B

echo.
echo ================================================
echo    INSTALLING DEPENDENCIES
echo ================================================
echo.
echo This will install required Python packages...
echo.

pip install streamlit pandas plotly python-dateutil

echo.
echo ================================================
echo    INSTALLATION COMPLETE!
echo ================================================
echo.
echo You can now run:
echo   - START_DEMO.bat (for demonstrations)
echo   - START_EVERYTHING.bat (for live use)
echo.

pause
