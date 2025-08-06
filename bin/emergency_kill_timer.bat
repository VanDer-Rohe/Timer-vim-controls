@echo off
echo Emergency Timer Shutdown Script
echo ================================
echo.

echo Step 1: Attempting graceful shutdown...
REM Try to close the timer window gracefully first
for /f "tokens=2" %%i in ('tasklist /v /fi "WINDOWTITLE eq HotkeyTimer*" /fo csv 2^>nul ^| find /v "WINDOWTITLE"') do (
    if not "%%i"=="PID" (
        echo Found timer process with PID %%i, attempting graceful close...
        taskkill /pid %%i >nul 2>&1
    )
)

timeout /t 2 /nobreak >nul

echo Step 2: Force killing any remaining Python processes...
REM Force kill Python processes
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

echo Step 3: Cleaning up any orphaned processes...
REM Kill any remaining timer-related processes
wmic process where "CommandLine like '%%timer_app.py%%'" delete >nul 2>&1

echo.
echo Timer cleanup complete!
echo.
echo If the timer is still running, try:
echo 1. Press Ctrl+Alt+Shift+Q (if AHK script is still running)
echo 2. Run this script again
echo 3. Restart your computer as last resort
echo.
pause
