from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QDialog
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from pysrc.dialogs import VimTimeInputDialog


class TimerWindow(QWidget):
    def __init__(self, initial_time=None):
        super().__init__()
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.is_hidden = False
        
        # Variables for dragging functionality
        self.dragging = False
        self.drag_start_position = None
        
        self.init_ui()
        
        # Only show window and get time if we should continue
        self.should_close = False
        
        if initial_time:
            self.set_timer_from_string(initial_time)
        else:
            # Get time from user first, before showing the main window
            if not self.get_time_from_user():
                # User cancelled, mark for closure
                self.should_close = True
    
    def init_ui(self):
        # Set window properties
        self.setWindowTitle("HotkeyTimer")  # Unique title for AHK to find
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint |
                          Qt.WindowType.Tool)
        
        # Set window size and background
        self.setFixedSize(200, 60)
        self.setStyleSheet("background-color: black;")
        
        # Set cursor to indicate draggable
        self.setCursor(Qt.CursorShape.SizeAllCursor)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create timer display label
        self.time_label = QLabel("00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set digital clock font style
        font = QFont("Consolas", 24, QFont.Weight.Bold)
        if not font.exactMatch():
            font = QFont("Courier New", 24, QFont.Weight.Bold)
        if not font.exactMatch():
            font = QFont("monospace", 24, QFont.Weight.Bold)
            
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: red;")
        
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        
        # Position window in top-right corner
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 20)
    
    def get_time_from_user(self):
        """Get timer duration from user input using vim-style controls"""
        dialog = VimTimeInputDialog(self)
        
        # Ensure dialog is properly focused when shown
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            time_str = dialog.get_time_string()
            self.set_timer_from_string(time_str)
            return True
        else:
            # User cancelled (pressed ESC or closed dialog)
            return False
    
    def set_timer_from_string(self, time_str):
        """Parse time string and set timer"""
        try:
            parts = time_str.split(':')
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                self.total_seconds = minutes * 60 + seconds
            elif len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                self.total_seconds = hours * 3600 + minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format")
            
            self.remaining_seconds = self.total_seconds
            self.update_display()
            self.start_timer()
            
        except ValueError:
            # If parsing fails, ask user again
            self.get_time_from_user()
    
    def start_timer(self):
        """Start the countdown timer"""
        if self.remaining_seconds > 0:
            self.timer.start(1000)  # Update every second
    
    def update_display(self):
        """Update the timer display"""
        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.time_label.setText("00:00")
            self.time_label.setStyleSheet("color: #FF6B6B; background-color: black;")
            return
        
        # Format time based on remaining duration
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        
        # Use HH:MM:SS if total time was >= 1 hour and remaining >= 1 hour
        # Use MM:SS if total time < 1 hour OR remaining < 1 hour
        if self.total_seconds >= 3600 and hours > 0:
            time_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_text = f"{minutes:02d}:{seconds:02d}"
        
        self.time_label.setText(time_text)
        self.remaining_seconds -= 1
    
    def toggle_visibility(self):
        """Toggle window visibility"""
        if self.is_hidden or not self.isVisible():
            self.show()
            self.raise_()
            self.activateWindow()
            self.is_hidden = False
        else:
            self.hide()
            self.is_hidden = True
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_H:
            self.toggle_visibility()
        super().keyPressEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPosition().toPoint() - self.pos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_start_position
            self.move(new_pos)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def enterEvent(self, event):
        """Handle mouse enter for visual feedback"""
        if not self.dragging:
            self.setStyleSheet("background-color: #111; border: 1px solid #333;")
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave to restore normal appearance"""
        if not self.dragging:
            self.setStyleSheet("background-color: black;")
        super().leaveEvent(event)
