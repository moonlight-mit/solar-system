@echo off
REM 🚀 Manual Server Startup
REM Use this if run.bat has issues or if you want to debug

echo.
echo 🚀 Solar System 3D - Manual Startup
echo ===================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo.
    echo Please run: .\run.bat
    echo Or create venv manually:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install --prefer-binary -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo.

REM Activate venv and show environment
call venv\Scripts\activate.bat
echo 📍 Using Python:
venv\Scripts\python --version
echo.

REM Run server
echo 🌌 Starting server...
echo    Open browser: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo    Press Ctrl+C to stop server
echo.

venv\Scripts\python app.py

pause
