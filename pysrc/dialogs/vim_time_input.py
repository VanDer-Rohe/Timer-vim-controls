from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QToolTip
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication


class VimTimeInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Timer')
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint |
                          Qt.WindowType.Tool)
        
        self.current_field = 0  # 0=hours, 1=minutes, 2=seconds
        self.help_visible = False  # Track help tooltip state
        self.init_ui()
        
    def init_ui(self):
        # Set dialog size and styling - increased height for better spacing
        self.setFixedSize(420, 120)
        self.setStyleSheet("""
            QDialog {
                background-color: black;
                color: red;
            }
            QLabel {
                color: red;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #333;
                color: red;
                border: 2px solid red;
                padding: 8px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
            }
            QLineEdit:focus {
                background-color: red;
                color: black;
                border: 2px solid #ff6666;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title label
        title_label = QLabel("Enter Timer Duration")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Time input layout
        time_layout = QHBoxLayout()
        
        # Hours field
        self.hours_field = QLineEdit("00")
        self.hours_field.setValidator(QIntValidator(0, 23))
        self.hours_field.setMaxLength(2)
        self.hours_field.setFixedWidth(80)
        self.hours_field.setFixedHeight(50)
        self.hours_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Minutes field  
        self.minutes_field = QLineEdit("05")
        self.minutes_field.setValidator(QIntValidator(0, 59))
        self.minutes_field.setMaxLength(2)
        self.minutes_field.setFixedWidth(80)
        self.minutes_field.setFixedHeight(50)
        self.minutes_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Seconds field
        self.seconds_field = QLineEdit("00")
        self.seconds_field.setValidator(QIntValidator(0, 59))
        self.seconds_field.setMaxLength(2)
        self.seconds_field.setFixedWidth(80)
        self.seconds_field.setFixedHeight(50)
        self.seconds_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Store fields in list for easy navigation
        self.fields = [self.hours_field, self.minutes_field, self.seconds_field]
        
        # Disable normal text editing - we'll handle all input via keyPressEvent
        for field in self.fields:
            field.setReadOnly(True)
            field.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Colon labels - vertically centered with the input fields
        colon1 = QLabel(":")
        colon1.setStyleSheet("font-size: 24px; font-weight: bold;")
        colon1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colon1.setFixedHeight(50)  # Match input field height
        
        colon2 = QLabel(":")
        colon2.setStyleSheet("font-size: 24px; font-weight: bold;")
        colon2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colon2.setFixedHeight(50)  # Match input field height
        
        # Add to layout with proper spacing
        time_layout.addStretch()
        time_layout.addWidget(self.hours_field)
        time_layout.addWidget(colon1)
        time_layout.addWidget(self.minutes_field)
        time_layout.addWidget(colon2)
        time_layout.addWidget(self.seconds_field)
        time_layout.addStretch()
        
        main_layout.addLayout(time_layout)
        
        # Info button layout
        info_layout = QHBoxLayout()
        info_layout.addStretch()
        
        # Info button (small circular button with "ⓘ")
        self.info_button = QLabel("ⓘ")
        self.info_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_button.setFixedSize(20, 20)
        self.update_info_button_style()
        self.info_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.info_button.mouseReleaseEvent = self.toggle_help
        
        info_layout.addWidget(self.info_button)
        main_layout.addLayout(info_layout)
        
        # Status label for feedback
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 10px; color: #ff6666;")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
        
        # Set focus to the dialog itself, not any field
        self.current_field = 1
        self.update_field_highlight()
        
        # Position dialog in center of screen
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() // 2 - self.width() // 2, screen.height() // 2 - self.height() // 2)
    
    def showEvent(self, event):
        """Called when dialog is shown - ensure proper focus"""
        super().showEvent(event)
        # Force the dialog to get focus and come to front
        self.raise_()
        self.activateWindow()
        self.setFocus()
        # Small delay to ensure window system processes the focus request
        QTimer.singleShot(10, self.force_focus)
    
    def force_focus(self):
        """Force focus with a slight delay"""
        self.raise_()
        self.activateWindow() 
        self.setFocus()
    
    def update_info_button_style(self):
        """Update info button style based on help visibility state"""
        if self.help_visible:
            # Active/pressed state
            style = """
                QLabel {
                    color: red;
                    font-size: 14px;
                    font-weight: bold;
                    border: 2px solid red;
                    border-radius: 10px;
                    background-color: #333;
                }
            """
        else:
            # Normal/inactive state
            style = """
                QLabel {
                    color: #888;
                    font-size: 14px;
                    font-weight: bold;
                    border: 1px solid #555;
                    border-radius: 10px;
                    background-color: #222;
                }
                QLabel:hover {
                    color: #ccc;
                    border-color: #777;
                    background-color: #333;
                }
            """
        self.info_button.setStyleSheet(style)
    
    def toggle_help(self, event):
        """Toggle help tooltip visibility"""
        if self.help_visible:
            # Hide help
            QToolTip.hideText()
            self.help_visible = False
        else:
            # Show help
            help_text = """<b>Timer Input Controls:</b><br><br>
<b>Navigation:</b><br>
• h - Move left<br>
• l - Move right<br><br>
<b>Value Control:</b><br>
• j - Decrease value<br>
• k - Increase value<br>
• 0-9 - Enter numbers<br>
• Backspace/Del - Clear field<br><br>
<b>Actions:</b><br>
• Enter - Start timer<br>
• Esc - Cancel<br><br>
<b>Click ⓘ again to hide</b>"""
            
            # Position tooltip
            tooltip_pos = self.info_button.mapToGlobal(self.info_button.rect().bottomLeft())
            QToolTip.showText(tooltip_pos, help_text, self.info_button)
            self.help_visible = True
        
        # Update button appearance
        self.update_info_button_style()
    
    def update_field_highlight(self):
        """Update visual highlighting of current field"""
        for i, field in enumerate(self.fields):
            if i == self.current_field:
                field.setStyleSheet("""
                    QLineEdit {
                        background-color: red;
                        color: black;
                        border: 3px solid #ff6666;
                        padding: 8px;
                        font-family: Consolas, 'Courier New', monospace;
                        font-size: 24px;
                        font-weight: bold;
                        text-align: center;
                    }
                """)
            else:
                field.setStyleSheet("""
                    QLineEdit {
                        background-color: #333;
                        color: red;
                        border: 2px solid red;
                        padding: 8px;
                        font-family: Consolas, 'Courier New', monospace;
                        font-size: 24px;
                        font-weight: bold;
                        text-align: center;
                    }
                """)
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key.Key_H:  # Move left
            self.move_field(-1)
        elif key == Qt.Key.Key_L:  # Move right
            self.move_field(1)
        elif key == Qt.Key.Key_J:  # Decrease value
            self.change_value(-1)
        elif key == Qt.Key.Key_K:  # Increase value
            self.change_value(1)
        elif key >= Qt.Key.Key_0 and key <= Qt.Key.Key_9:  # Number keys
            self.enter_digit(key - Qt.Key.Key_0)
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # Only accept if we have a valid time
            if self.is_valid_time():
                self.accept()
            else:
                # Show error message for invalid time
                self.status_label.setText("Timer must be greater than 00:00:00")
                QTimer.singleShot(2000, lambda: self.status_label.setText(""))  # Clear after 2 seconds
        elif key == Qt.Key.Key_Escape:
            # Properly reject the dialog
            self.reject()
        elif key == Qt.Key.Key_Backspace or key == Qt.Key.Key_Delete:
            # Clear current field
            self.clear_current_field()
        else:
            # Don't allow any other keys to be processed by the fields
            # This prevents normal text editing
            pass
    
    def move_field(self, direction):
        """Move focus between fields (h/l navigation)"""
        self.current_field = (self.current_field + direction) % 3
        self.update_field_highlight()
    
    def change_value(self, delta):
        """Increase/decrease current field value (j/k navigation)"""
        current_widget = self.fields[self.current_field]
        try:
            current_value = int(current_widget.text() or "0")
        except ValueError:
            current_value = 0
        
        # Set limits based on field
        if self.current_field == 0:  # Hours
            max_val = 23
        else:  # Minutes or seconds
            max_val = 59
        
        new_value = max(0, min(max_val, current_value + delta))
        current_widget.setText(f"{new_value:02d}")
    
    def enter_digit(self, digit):
        """Enter a digit in the current field"""
        current_widget = self.fields[self.current_field]
        current_text = current_widget.text()
        
        # If field is empty or "00", replace with the digit
        if current_text == "00" or current_text == "":
            new_text = f"0{digit}"
        else:
            # Shift left and add new digit (like a calculator)
            try:
                current_value = int(current_text)
                # Move left digit to tens place, add new digit to ones place
                new_value = (current_value % 10) * 10 + digit
                
                # Check limits based on field
                if self.current_field == 0:  # Hours
                    max_val = 23
                else:  # Minutes or seconds
                    max_val = 59
                
                if new_value <= max_val:
                    new_text = f"{new_value:02d}"
                else:
                    # If it would exceed limit, just use the single digit
                    new_text = f"0{digit}"
            except ValueError:
                new_text = f"0{digit}"
        
        current_widget.setText(new_text)
    
    def clear_current_field(self):
        """Clear the current field (set to 00)"""
        current_widget = self.fields[self.current_field]
        current_widget.setText("00")
    
    def get_time_string(self):
        """Get the time as HH:MM:SS string"""
        hours = self.hours_field.text().zfill(2)
        minutes = self.minutes_field.text().zfill(2)
        seconds = self.seconds_field.text().zfill(2)
        return f"{hours}:{minutes}:{seconds}"
    
    def is_valid_time(self):
        """Check if the current time is valid (not all zeros)"""
        try:
            hours = int(self.hours_field.text() or "0")
            minutes = int(self.minutes_field.text() or "0")
            seconds = int(self.seconds_field.text() or "0")
            return hours > 0 or minutes > 0 or seconds > 0
        except ValueError:
            return False
