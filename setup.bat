@echo off
REM SkillSnap Backend Setup Script for Windows

echo 🚀 Setting up SkillSnap Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

echo ✓ Python detected

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv skillsnap_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call skillsnap_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📋 Installing dependencies...
pip install -r requirements.txt

REM Download spaCy model
echo 🤖 Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo ✅ Setup complete!
echo.
echo To start the server:
echo   1. Activate the virtual environment: skillsnap_env\Scripts\activate
echo   2. Run the application: python app.py
echo.
echo To deactivate the virtual environment when done: deactivate
pause 