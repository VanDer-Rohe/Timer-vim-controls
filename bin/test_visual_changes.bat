@echo off
echo Testing visual improvements...
echo.
echo Starting timer with new borderless input dialog...
echo (Close the timer after you see it working)
echo.
pause

"..\\.venv\Scripts\python.exe" ..\timer_app.py

echo.
echo Test completed! The timer should have:
echo 1. Borderless input dialog with black/red styling
echo 2. No terminal window popup
echo 3. Working hide/show functionality
echo.
pause
