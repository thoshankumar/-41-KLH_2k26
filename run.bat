@echo off
REM AI Behavioral Finance Coach - Run Script for Windows
REM Makes it easy to start the application

echo.
echo 🏦 AI Behavioral Finance Coach
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✓ pip found
echo.

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Dependencies not installed. Installing now...
    pip install -r requirements.txt
    echo.
)

echo ✓ All dependencies installed
echo.

REM Start the application
echo 🚀 Starting AI Behavioral Finance Coach...
echo.
echo The application will open in your browser at:
echo http://localhost:8501
echo.
echo Demo Account:
echo   Email: demo@financecoach.ai
echo   Password: demo123
echo.
echo Press Ctrl+C to stop the application
echo.
echo ================================
echo.

streamlit run app.py
