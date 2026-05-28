@echo off
echo ============================================================
echo Cirrhosis Prediction System - Installation and Launch
echo ============================================================
echo.

echo Step 1: Checking Python installation...
py --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)
echo Python is installed!
echo.

echo Step 2: Installing required packages...
echo This may take a few minutes...
echo.
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo.
echo All packages installed successfully!
echo.

echo Step 3: Running setup verification...
py test_setup.py
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Starting the application...
echo The model will be trained on first run (takes 10-30 seconds)
echo.
echo After the server starts, open your browser to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when you're done.
echo ============================================================
echo.
pause
echo Starting server...
py app.py
