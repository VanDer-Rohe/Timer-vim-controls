@echo off
echo ===============================================
echo   Timer Hotkeys Auto-Start Removal
echo ===============================================
echo.
echo Checking for existing auto-start installations...
echo.

set "StartupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "StartupFile=%StartupFolder%\hotkey_timer.ahk"
set "FoundAny=0"

REM Check startup folder
if exist "%StartupFile%" (
    echo Found: Startup folder installation
    del "%StartupFile%"
    if %ERRORLEVEL% EQU 0 (
        echo - Removed from startup folder successfully
        set "FoundAny=1"
    ) else (
        echo - ERROR: Failed to remove from startup folder
    )
) else (
    echo - No startup folder installation found
)

REM Check registry
reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "TimerHotkeys" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found: Registry installation
    reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "TimerHotkeys" /f >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo - Removed from registry successfully
        set "FoundAny=1"
    ) else (
        echo - ERROR: Failed to remove from registry
    )
) else (
    echo - No registry installation found
)

echo.
if "%FoundAny%"=="1" (
    echo SUCCESS: Auto-start has been disabled!
    echo Timer hotkeys will no longer start automatically with Windows.
) else (
    echo No auto-start installations were found.
    echo Timer hotkeys are not currently set to start automatically.
)

echo.
echo Press any key to exit...
pause > nul
