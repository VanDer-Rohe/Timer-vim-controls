# Hotkey Timer Application

A simple countdown timer application that can be triggered via hotkeys using AutoHotkey and displays a clean digital clock interface.

## Quick Setup

1. **Clone the repository**
2. **Run the setup script**: `bin\setup.bat`
   - This will automatically create a Python virtual environment
   - Install all required dependencies
   - No manual Python setup required!
3. **Start using the timer**: `bin\start_timer_hotkeys.bat`

## Features

- **Global Hotkeys**: Start timer from anywhere with Ctrl+Alt+T
- **Vim-style Controls**: Use h/j/k/l for navigation and editing in the input dialog
- **Number Input**: Direct number entry (0-9) in timer fields
- **Draggable Timer**: Click and drag the timer window to reposition it
- **Clean Digital Display**: Black background, red digital font, no borders
- **Borderless Input Dialog**: Matching aesthetic for time input with info button
- **Silent Operation**: No terminal popups when launched via hotkeys
- **Smart Time Format**: 
  - Shows HH:MM:SS for timers ≥ 1 hour
  - Shows MM:SS for timers < 1 hour
  - Automatically switches from HH:MM:SS to MM:SS when timer goes below 1 hour
- **Always on Top**: Timer stays visible above other windows
- **Hide/Show Toggle**: Ctrl+Alt+H to hide/show timer

## Prerequisites

- **Python 3.8+**: Download from https://python.org
- **AutoHotkey**: Download from https://autohotkey.com

## Detailed Setup (Alternative to Quick Setup)

If you prefer manual setup:

1. **Install Python Dependencies**:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install AutoHotkey** (if not already installed):
   - Download from https://www.autohotkey.com/
   - Install the application

3. **Configure Python Path** (if needed):
   - Open `hotkey_timer.ahk`
   - Modify the `PythonPath` variable if your Python executable is not in PATH

4. **Set up Auto-start (Optional)**:
   - Run `bin\install_autostart.bat` and choose your preferred method:
     - **Startup Folder** (Recommended): Copies script to Windows startup folder
     - **Registry Entry**: Adds registry entry for auto-start
   - To disable auto-start: Run `bin\uninstall_autostart.bat` (automatically detects and removes both methods)

## Usage

### Starting the Application

**Auto-start (Recommended)**:
- Run `bin\install_autostart.bat` once to set up automatic startup
- Timer hotkeys will be available immediately after Windows boot

**Manual start**:
1. **Run the AutoHotkey Script**:
   - Double-click `hotkey_timer.ahk`
   - Or run `start_timer_hotkeys.bat` (backup method)

2. **Use Hotkeys**:
   - **Ctrl + Alt + T**: Start new timer
   - **Ctrl + Alt + H**: Toggle timer visibility
   - **Ctrl + Alt + Q**: Close timer (graceful)
   - **Ctrl + Alt + Shift + Q**: Emergency kill all timer processes (force)

## Emergency Shutdown

If the timer becomes unresponsive or you can't close it:

1. **Emergency Hotkey**: Press `Ctrl + Alt + Shift + Q` (if AHK is still running)
2. **Kill Scripts**: 
   - Run `emergency_kill_timer.bat` (tries graceful first, then force)
   - Run `kill_timer.bat` (immediate force kill)
3. **Manual**: Open Task Manager and end all `python.exe` processes

### Timer Controls

When the timer input dialog appears:
- **Navigation**: 
  - `h` - Move left to previous field
  - `l` - Move right to next field
- **Value Control**:
  - `j` - Decrease current field value
  - `k` - Increase current field value
  - `0-9` - Enter numbers directly (calculator-style)
  - `Backspace/Delete` - Clear current field to 00
- **Confirmation**:
  - `Enter` - Start timer with current values
  - `Esc` - Cancel timer creation

**Input Fields**: Separate HH:MM:SS fields (no need to type colons)
- Default starts with 00:05:00 (5 minutes)
- Hours: 0-23, Minutes/Seconds: 0-59
- Focus starts on minutes field (most commonly changed)
- **Number Entry**: Type digits to enter values (e.g., type "1" then "5" for "15")

### Timer Window Controls

- **ESC Key**: Close timer
- **H Key**: Toggle visibility
- **Mouse Drag**: Click and drag anywhere on the timer to move it around the screen
- **Hover Effect**: Timer background changes slightly when you hover over it
- Timer automatically closes when countdown reaches zero

## Examples

- `05:00` - 5 minute timer
- `01:30` - 1 minute 30 seconds
- `01:30:00` - 1 hour 30 minutes
- `00:10:30` - 10 minutes 30 seconds

## Command Line Usage

You can also run the timer directly from command line:

```cmd
python timer_app.py --time "05:00"
python timer_app.py --time "01:30:00" --hide
```

Options:
- `--time` or `-t`: Set timer duration
- `--hide`: Start timer hidden

## Customization

Edit `timer_app.py` to customize:
- Font size and family
- Colors (background, text)
- Window size and position
- Timer behavior

## Troubleshooting

1. **Timer doesn't start**: Check that Python is in your PATH or update the `PythonPath` in the AHK script
2. **PyQt6 errors**: Install PyQt6 with `pip install PyQt6`
3. **Hotkeys don't work**: Make sure AutoHotkey script is running (check system tray)
