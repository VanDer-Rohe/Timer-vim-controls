; AutoHotkey Script for Timer Application
; Hotkey: Ctrl + Alt + T to start timer
; Hotkey: Ctrl + Alt + H to toggle timer visibility

#NoEnv
#SingleInstance Force
#Persistent

; Set the path to your Python executable and script
PythonPath := A_ScriptDir . "\.venv\Scripts\python.exe"
ScriptPath := A_ScriptDir . "\timer_app.py"

; Global variable to track if timer is running
TimerPID := 0

; Ctrl + Alt + T: Start new timer
^!t::
    ; Check if a timer is already running
    if (TimerPID != 0) {
        Process, Exist, %TimerPID%
        if (ErrorLevel) {
            ; Timer is still running, bring it to front
            WinShow, HotkeyTimer
            WinActivate, HotkeyTimer
            return
        } else {
            ; Process no longer exists, reset PID
            TimerPID := 0
        }
    }
    
    ; Start new timer (Hide=true hides the command prompt window)
    Run, %PythonPath% "%ScriptPath%", , Hide, NewPID
    TimerPID := NewPID
    
    ; Give the application a moment to start, then ensure it gets focus
    Sleep, 500
    WinWait, Set Timer, , 3  ; Wait up to 3 seconds for the dialog
    if (ErrorLevel = 0) {
        WinActivate, Set Timer
    }
return

; Ctrl + Alt + H: Toggle timer visibility (if running)
^!h::
    if (TimerPID != 0) {
        Process, Exist, %TimerPID%
        if (ErrorLevel) {
            ; Target the specific timer window by title
            IfWinExist, HotkeyTimer
            {
                IfWinActive, HotkeyTimer
                {
                    WinHide, HotkeyTimer
                }
                else
                {
                    WinShow, HotkeyTimer
                    WinActivate, HotkeyTimer
                }
            }
            else
            {
                ; Window might be hidden, try to show it
                WinShow, HotkeyTimer
                WinActivate, HotkeyTimer
            }
        } else {
            ; Process no longer exists, reset PID
            TimerPID := 0
        }
    }
return

; Ctrl + Alt + Q: Close timer
^!q::
    if (TimerPID != 0) {
        Process, Close, %TimerPID%
        TimerPID := 0
    }
return

; Ctrl + Alt + Shift + Q: Emergency kill all timer processes
^!+q::
    ; Force kill all Python processes
    Run, taskkill /f /im python.exe, , Hide
    Run, taskkill /f /im pythonw.exe, , Hide
    
    ; Reset the PID since we just killed everything
    TimerPID := 0
    
    ; Show confirmation
    TrayTip, Timer Killed, All timer processes have been forcefully terminated., 3
return

; Optional: Show help message on startup
; You can comment this out if you don't want the help message
; MsgBox, 4096, Timer Hotkeys, 
; (
; Timer Application Hotkeys:
; 
; Ctrl + Alt + T : Start new timer
; Ctrl + Alt + H : Toggle timer visibility
; Ctrl + Alt + Q : Close timer
; 
; The timer window also responds to:
; ESC : Close timer
; H   : Toggle visibility
; ), 3
