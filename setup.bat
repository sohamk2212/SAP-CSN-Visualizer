@echo off
REM Setup script for CSN Object Visualizer (Windows)

echo.
echo 🧩 CSN Object Visualizer - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

for /f \"tokens=*\" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python detected: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist \".venv\" (
    echo ⚠️  Virtual environment already exists. Using existing environment.
) else (
    python -m venv .venv
    echo ✓ Virtual environment created
)

echo.

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call .venv\\Scripts\\activate.bat
echo ✓ Virtual environment activated

echo.

REM Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✓ Pip upgraded

echo.

REM Install requirements
echo 📚 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully

echo.

REM Verify installation
echo 🔍 Verifying installation...
python -c \"import streamlit; import pandas; import openpyxl\" 2>nul
if errorlevel 1 (
    echo ⚠️  Some dependencies may not be properly installed
) else (
    echo ✓ All dependencies verified
)

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo 📝 Next Steps:
echo.
echo 1. Activate the virtual environment (if not already active):
echo    .venv\\Scripts\\activate.bat
echo.
echo 2. Run the application:
echo    streamlit run app.py
echo.
echo 3. Open your browser to: http://localhost:8501
echo.
echo 📖 For more information, see README.md
echo.
pause
