@echo off
echo Starting SecureBank Pro...
echo.
cd /d "%~dp0"
echo Activating Python environment...
call "..\..\..\.venv\Scripts\activate.bat"
echo.
echo Launching Streamlit application...
streamlit run bank_management_app.py
pause
