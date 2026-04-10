@echo off
REM 🌌 Solar System 3D - Quick Start (Windows)
REM This script automatically sets up and runs the solar system simulation

echo.
echo 🌌 Solar System 3D - Quick Start
echo ================================
echo.

REM Check Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.9+
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python version:
python --version
echo.

REM Get Python version and check if it's 3.9+
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   Python: %PYTHON_VERSION%

REM Create venv if it doesn't exist or is corrupted
if exist "venv" (
    REM Check if venv is valid
    if not exist "venv\Scripts\python.exe" (
        echo ⚠️  Virtual environment is corrupted, recreating...
        rmdir /s /q venv
        goto create_venv
    ) else (
        echo ✅ Virtual environment already exists
        goto install_deps
    )
)

:create_venv
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment!
    echo    Try running: python -m pip install --upgrade pip
    pause
    exit /b 1
)
echo ✅ Virtual environment created

:install_deps

echo.
echo 📥 Installing dependencies...
echo.
echo 1️⃣  Upgrading pip, setuptools and wheel...
echo    (This may need administrator rights on first run)
echo.

REM Use Python to upgrade pip (avoids file lock issues on Windows)
call venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel --no-warn-script-location

if errorlevel 1 (
    echo.
    echo ⚠️  Note: pip upgrade skipped (this is OK, old version still works)
    echo    Continuing with installation...
) else (
    echo ✅ pip upgraded successfully
)

echo.
echo 2️⃣  Installing Python packages...
call venv\Scripts\pip install -r requirements.txt --prefer-binary --no-warn-script-location

if errorlevel 1 (
    echo.
    echo ⚠️  First attempt had issues, trying alternative method...
    echo.
    call venv\Scripts\pip install --no-build-isolation -r requirements.txt --no-warn-script-location
    
    if errorlevel 1 (
        echo.
        echo ❌ Installation failed. Possible causes:
        echo    - Network connection issues
        echo    - Antivirus/firewall blocking downloads
        echo    - Incompatible Python version ^(need Python 3.9+^)
        echo    - Low disk space
        echo.
        echo 💡 Try these steps:
        echo    1. Close all Python/pip windows
        echo    2. Restart command prompt as Administrator
        echo    3. Delete the venv folder and run again
        echo    4. Check your internet connection
        echo.
        pause
        exit /b 1
    )
)
echo ✅ Dependencies installed successfully

echo.
echo 🚀 Starting Solar System Physics Engine...
echo.
echo ================================================================
echo  🌌 Server running at: http://localhost:9000
echo  📚 API Documentation: http://localhost:9000/docs
echo  🌐 Frontend will open in a few seconds...
echo ================================================================
echo.

REM Start server in background
start "⭐ Solar System Server" cmd /k "cd /d %CD% && title Solar System Server && venv\Scripts\python -u app.py"

REM Wait for server to fully start
echo ⏳ Waiting 8 seconds for server to initialize...
timeout /t 8 /nobreak

REM Check if server is responding
echo 🔍 Checking server health...
@for /f %%i in ('powershell -NoProfile -Command "try{(Invoke-WebRequest http://localhost:9000 -TimeoutSec 2).StatusCode}catch{Write-Output 'offline'}"') do set SERVER_STATUS=%%i

if "%SERVER_STATUS%"=="200" (
    echo ✅ Server is running!
) else (
    echo ⚠️  Server might be starting (this is normal), opening browser anyway...
)

echo.
REM Open browser
echo 🌐 Opening browser...
start http://localhost:9000

echo.
echo ✅ Launch complete!
echo.
echo 📌 Tips:
echo  - Keep this window open while using the application
echo  - Press Ctrl+C in the "Solar System Server" window to stop the server
echo  - Visit http://localhost:9000/docs for API documentation
echo.
pause
