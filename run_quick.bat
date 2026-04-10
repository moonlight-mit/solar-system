@echo off
REM 🚀 QUICK START - Skip pip upgrade (for when pip is locked)
REM Use this if run.bat fails on pip upgrade

echo.
echo 🚀 Solar System 3D - Quick Install (Skip Pip Upgrade)
echo =======================================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create venv
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment found
)

echo.
echo 📥 Installing packages directly (skipping pip upgrade)...
echo.

REM Install packages without upgrading pip first
call venv\Scripts\pip install -r requirements.txt --prefer-binary --disable-pip-version-check

if errorlevel 1 (
    echo.
    echo ⚠️  Trying alternative method...
    call venv\Scripts\pip install --no-build-isolation -r requirements.txt --disable-pip-version-check
    
    if errorlevel 1 (
        echo ❌ Installation failed
        echo.
        echo Try these troubleshooting steps:
        echo   1. Close all Python windows
        echo   2. Right-click Command Prompt and select "Run as Administrator"
        echo   3. Delete the venv folder: rmdir /s /q venv
        echo   4. Run this script again
        echo.
        pause
        exit /b 1
    )
)

echo ✅ All packages installed successfully!
echo.
echo 🚀 Starting server...
echo    - Server: http://localhost:9000
echo    - API Docs: http://localhost:9000/docs
echo.

REM Start server
start "⭐ Solar System Server" cmd /k "cd /d %CD% && title Solar System Server && venv\Scripts\python -u app.py"

timeout /t 6 /nobreak

REM Open browser
start http://localhost:9000

echo.
echo ✅ Done! Check the browser window opening...
echo.
pause
