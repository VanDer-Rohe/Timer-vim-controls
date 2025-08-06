@echo off
echo ===============================================
echo    Timer Hotkeys Auto-Start Installation
echo ===============================================
echo.
echo Choose installation method:
echo.
echo 1. Startup Folder (Recommended)
echo    - Copies script to Windows startup folder
echo    - Easy to see and remove manually
echo    - Works like any other startup program
echo.
echo 2. Windows Registry
echo    - Adds registry entry for auto-start
echo    - More "integrated" but harder to find
echo    - Requires registry editing to remove manually
echo.
echo 3. Cancel installation
echo.

:choice
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto startup_folder
if "%choice%"=="2" goto registry
if "%choice%"=="3" goto cancel
echo Invalid choice. Please enter 1, 2, or 3.
goto choice

:startup_folder
echo.
echo Installing via Startup Folder method...
echo.

REM Get the startup folder path
set "StartupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Copy the AHK script to startup folder
copy "%~dp0..\hotkey_timer.ahk" "%StartupFolder%\hotkey_timer.ahk"

if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Timer hotkeys will now start automatically when Windows boots!
    echo.
    echo The AHK script has been copied to:
    echo %StartupFolder%
    echo.
    echo To disable auto-start:
    echo - Delete the file from the startup folder, or
    echo - Run: bin\uninstall_autostart.bat
) else (
    echo ERROR: Failed to copy file to startup folder.
    echo You may need to run this as administrator.
)
goto end

:registry
echo.
echo Installing via Windows Registry method...
echo.

REM Add registry entry for current user
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "TimerHotkeys" /t REG_SZ /d "\"%~dp0..\hotkey_timer.ahk\"" /f

if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Timer hotkeys added to Windows startup registry!
    echo.
    echo To disable auto-start, run: bin\uninstall_autostart.bat
) else (
    echo ERROR: Failed to add registry entry.
    echo You may need to run this as administrator.
)
goto end

:cancel
echo.
echo Installation cancelled.
goto end

:end
echo.
echo Press any key to exit...
pause > nul
