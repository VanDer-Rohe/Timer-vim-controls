import sys
from PyQt6.QtWidgets import QApplication
from pysrc.widgets import TimerWindow
from pysrc.utils import parse_arguments


def main():
    args = parse_arguments()
    
    app = QApplication(sys.argv)
    
    # Ensure the application can get focus even when launched from background
    app.setQuitOnLastWindowClosed(True)
    
    # Create timer window
    timer_window = TimerWindow(args.time)
    
    # Check if user cancelled during initialization
    if timer_window.should_close:
        # User pressed ESC, exit immediately without showing anything
        sys.exit(0)
    
    if args.hide:
        timer_window.hide()
        timer_window.is_hidden = True
    else:
        timer_window.show()
        # Ensure window gets focus when shown
        timer_window.raise_()
        timer_window.activateWindow()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
