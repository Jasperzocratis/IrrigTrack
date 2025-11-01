@echo off
echo ========================================
echo Starting Python ML API Server
echo ========================================
echo.

REM Check if Python is installed (try py first, then python)
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed or not in PATH
        echo.
        echo Please install Python from: https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

echo Python found:
%PYTHON_CMD% --version
echo.

REM Check if virtual environment exists
if not exist "ml_api_env" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv ml_api_env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call ml_api_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade requirements
echo Installing dependencies...
python -m pip install -q --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

python -m pip install -q -r requirements_ml_api.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check requirements_ml_api.txt
    pause
    exit /b 1
)

REM Start the server (using NumPy-only version for compatibility)
echo.
echo ========================================
echo Starting ML API server on port 5000...
echo Using: ml_api_server_simple.py (NumPy Linear Regression)
echo ========================================
echo.
python ml_api_server_simple.py

pause

