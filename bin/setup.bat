@echo off
echo Setting up HotkeyTimer Python environment...
echo.

REM Change to project root directory
cd /d "%~dp0\.."

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install requirements
echo.
echo Installing dependencies...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo SUCCESS: Setup completed successfully!
echo.
echo You can now run the timer using:
echo   1. bin\start_timer_hotkeys.bat  (to start hotkeys)
echo   2. bin\test_timer.bat           (to test the timer)
echo.
echo To install autostart, run one of:
echo   - bin\install_autostart.bat
echo   - bin\install_autostart_registry.bat
echo.
pause
