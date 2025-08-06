@echo off
echo Testing Timer Application...
echo.

echo Testing help command:
C:\Code\ahkScripts\Timer\.venv\Scripts\python.exe ..\timer_app.py --help
echo.

echo Testing with 5-second timer (close the timer window when it appears):
echo Press any key to start the test...
pause > nul

C:\Code\ahkScripts\Timer\.venv\Scripts\python.exe ..\timer_app.py --time "00:05"

echo.
echo Test completed!
pause
