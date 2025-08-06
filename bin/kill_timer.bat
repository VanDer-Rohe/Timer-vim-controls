@echo off
echo Killing Timer Application...
echo.

REM Kill all Python processes (this will kill the timer)
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

REM Kill any processes with "timer" in the name
taskkill /f /fi "IMAGENAME eq *timer*" >nul 2>&1

REM Kill any PyQt applications that might be the timer
for /f "tokens=2" %%i in ('tasklist /fi "IMAGENAME eq python.exe" /fo csv ^| find "python.exe"') do (
    taskkill /f /pid %%i >nul 2>&1
)

REM Kill any processes with HotkeyTimer window title
for /f "tokens=2" %%i in ('tasklist /v /fi "WINDOWTITLE eq HotkeyTimer*" /fo csv 2^>nul ^| find /v "WINDOWTITLE"') do (
    if not "%%i"=="PID" taskkill /f /pid %%i >nul 2>&1
)

echo Timer application should now be terminated.
echo.

REM Also kill the AutoHotkey script if it's running
taskkill /f /fi "IMAGENAME eq AutoHotkey*" >nul 2>&1
echo AutoHotkey script also terminated.
echo.

echo All timer-related processes have been killed.
echo You can now restart the timer with start_timer_hotkeys.bat
echo.
pause
