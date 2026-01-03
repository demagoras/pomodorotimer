from datetime import timedelta
from enum import Enum
from pathlib import Path
import sys

from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QTimer, QUrl 
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget
)

BASE_DIR = Path(__file__).resolve().parent
        
class WorkState(Enum):
    WORKING = 1
    GRACE = 2
    BREAK = 3

class MainWindow(QMainWindow):
    """Main application window for the Pomodoro Timer."""
    def __init__(self):
        super().__init__()

        # -- Time constants & boolean flags --
        self.TICK_INTERVAL = 1000 # milliseconds
        self.WORK_TIME = timedelta(minutes = 25)
        self.BREAK_TIME = timedelta(minutes = 5)
        self.GRACE_TIME = timedelta(seconds = 10)

        self.work_topic = "Topic Name"
        self.state = WorkState.WORKING

        # -- Animation Constants --
        self.SHAKE_DURATION = 50   # ms per shake
        self.SHAKE_COUNT = 3       # number of shakes
        self.SHAKE_DISTANCE = 8    # pixels to the side

        # -- Style constants --
        self.FONT_SIZE_TOPIC = "24px"
        self.FONT_SIZE_TIMER = "48px"

        self.COLOR_WORK = "white"
        self.COLOR_GRACE = "orange"
        self.COLOR_BREAK = "green"

        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(300, 200)

        self.topic_label = QLineEdit(self.work_topic)
        self.topic_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.topic_label.setStyleSheet(f"""
            font-size: {self.FONT_SIZE_TOPIC};
            border: none;
            background: transparent;
        """)
        self.topic_label.textChanged.connect(self.update_topic)

        self.timer_label = QLineEdit()
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet(f"""
            font-size: {self.FONT_SIZE_TIMER};
            border: none;
            background: transparent;
        """)
        self.timer_label.setReadOnly(True)
        self.timer_label.focusInEvent = self.enter_edit_mode
        self.timer_label.focusOutEvent = self.exit_edit_mode

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.toggle_time_button = QPushButton("Start")
        self.reset_button = QPushButton("Reset")
        self.toggle_time_button.clicked.connect(self.toggle_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        filename_time_over = BASE_DIR / "sounds" / "bell.wav"
        self.time_over_sound = QSoundEffect(self)
        self.time_over_sound.setSource(QUrl.fromLocalFile(str(filename_time_over)))

        # Although the C++ engine does it automatically
        # Some won't have access to the console to see errors
        if self.time_over_sound.status() == QSoundEffect.Status.Error:
            print(f"Error loading sound: {filename_time_over}")

        # -- Layout Management --
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.toggle_time_button)
        buttons_layout.addWidget(self.reset_button)

        layout = QVBoxLayout()
        layout.addWidget(self.topic_label)
        layout.addWidget(self.timer_label)
        layout.addLayout(buttons_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.reset_timer()

    # --- BUTTON SLOTS ---
    def toggle_timer(self):
        """Toggles the timer between running and paused states."""
        if self.timer.isActive():
            self.timer.stop()
            self.toggle_time_button.setText("Resume")
        else:
            self.timer.start(self.TICK_INTERVAL) # Not amazing but good enough
            self.toggle_time_button.setText("Pause")

    def reset_timer(self):
        """Resets everything to the initial state."""
        self.timer.stop()
        self.time_over_sound.stop()

        self.remaining_time = self.WORK_TIME
        self.update_timer_label()
        self.topic_label.setText(self.work_topic)

        self.toggle_time_button.setText("Start")
        self.toggle_time_button.setEnabled(True)
        self.state = WorkState.WORKING
        self.apply_topic_style(self.COLOR_WORK)
    
    # --- EDIT MODE HANDLERS ---
    def enter_edit_mode(self, e):
        """Switch to edit mode: show HH:MM:SS format with all digits."""
        if (not self.timer.isActive() and
            self.toggle_time_button.text() != "Resume"):
            self.timer_label.setReadOnly(False)
            total_seconds = int(self.remaining_time.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            mins, secs = divmod(remainder, 60)
            self.timer_label.setText(f"{hours:02d}:{mins:02d}:{secs:02d}")
            self.timer_label.textChanged.connect(self.format_time_input)

            # Force cursor to end of text on click
            def lock_cursor_to_end(e):
                QLineEdit.mousePressEvent(self.timer_label, e)
                self.timer_label.setCursorPosition(
                    len(self.timer_label.text())
                )
            
            self.timer_label.mousePressEvent = lock_cursor_to_end

        QLineEdit.focusInEvent(self.timer_label, e)

    def exit_edit_mode(self, e):
        """Switch back to display mode."""
        try:
            self.timer_label.textChanged.disconnect(self.format_time_input)
        except (TypeError, RuntimeError):
            pass
        
        if not self.parse_manual_input():
            self.shake_window()

        self.timer_label.setReadOnly(True)
        self.update_timer_label()
        QLineEdit.focusOutEvent(self.timer_label, e)

    def format_time_input(self, text):
        """Keep only digits and format as HHMMSS (shifts left as you type)."""
        # Remove non-digit characters, limit to only 6, and format with colons
        digits = ''.join(c for c in text if c.isdigit())
        digits = digits[-6:].zfill(6)
        formatted = f"{digits[0:2]}:{digits[2:4]}:{digits[4:6]}"

        # Prevent an infinite recursion loop
        self.timer_label.textChanged.disconnect(self.format_time_input)
        self.timer_label.setText(formatted)
        self.timer_label.setCursorPosition(len(formatted))
        self.timer_label.textChanged.connect(self.format_time_input)
    
    def parse_manual_input(self):
        """Converts the formatted text back into a timedelta"""
        text = self.timer_label.text().replace(':', '')
        if len(text) == 6 and text.isdigit():
            hours = int(text[0:2])
            mins = int(text[2:4])
            secs = int(text[4:6])

            if hours == 0 and mins == 0 and secs == 0:
                return False
            
            if hours == 99 and mins == 99 and secs == 99:
                hours = 99
                mins = 59
                secs = 59

            self.remaining_time = timedelta(
                hours=hours, minutes=mins, seconds=secs
            )
            return True
        return False

    def shake_window(self):
        """Animates the window shaking to indicate an error."""
        self.shake_anim = QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(self.SHAKE_DURATION)
        self.shake_anim.setLoopCount(self.SHAKE_COUNT)

        start_pos = self.pos()

        # Shake path: Start -> Slightly Left -> Slightly Right -> Start
        # 0 is the start, 1 is the end of the animation loop
        self.shake_anim.setKeyValueAt(0, start_pos)
        self.shake_anim.setKeyValueAt(0.25, start_pos + QPoint(-5, 0))
        self.shake_anim.setKeyValueAt(0.75, start_pos + QPoint(5, 0))
        self.shake_anim.setKeyValueAt(1, start_pos)

        self.shake_anim.start()

    # --- UI HELPERS ---
    def update_timer(self):
        """Update the timer display every second."""
        if self.remaining_time.total_seconds() > 0:
            self.remaining_time -= timedelta(milliseconds=self.TICK_INTERVAL)
            self.update_timer_label()
        else: # Time is over
            self.handle_transition()

    def apply_topic_style(self, color):
        """Standardized styling to keep handle_transition clean."""
        style = f"""
            font-size: {self.FONT_SIZE_TOPIC};
            color: {color};
            border: none;
            background: transparent;
        """
        self.topic_label.setStyleSheet(style)

    def update_timer_label(self):
        """Handles the format MM:SS or H:MM:SS for the timer label."""
        total_seconds = int(self.remaining_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        mins, secs = divmod(remainder, 60)
        
        if self.remaining_time >= timedelta(hours=1):
            self.timer_label.setText(f"{hours}:{mins:02d}:{secs:02d}")
        else:
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")
    
    def update_topic(self, text):
        """Updates the work topic based on user input."""
        self.work_topic = text

    # --- STATE TRANSITIONS ---
    def handle_transition(self):
        """Handles the transition between work and break periods."""
        self.time_over_sound.setLoopCount(1) # Play sound once

        if self.state == WorkState.WORKING:
            self.transition_to_grace()
        elif self.state == WorkState.GRACE:
            self.transition_to_break()
        else:
            self.transition_to_work()
        
        self.update_timer_label()
    
    def transition_to_grace(self):
        """Transition from WORKING to GRACE period."""
        self.state = WorkState.GRACE
        self.time_over_sound.play()
        self.remaining_time = self.GRACE_TIME
        self.topic_label.textChanged.disconnect()
        self.topic_label.setEnabled(False)
        self.topic_label.setText("Prepare for a break")
        self.apply_topic_style(self.COLOR_GRACE)
        self.toggle_time_button.setEnabled(False)
    
    def transition_to_break(self):
        """Transition from GRACE to BREAK period."""
        self.state = WorkState.BREAK
        self.remaining_time = self.BREAK_TIME
        self.topic_label.setText("Break Time!")
        self.apply_topic_style(self.COLOR_BREAK)
    
    def transition_to_work(self):
        self.state = WorkState.WORKING
        self.time_over_sound.play()
        self.remaining_time = self.WORK_TIME
        self.topic_label.setText(self.work_topic)
        self.topic_label.setEnabled(True)
        self.topic_label.textChanged.connect(self.update_topic)
        self.apply_topic_style(self.COLOR_WORK)
        self.toggle_time_button.setEnabled(True)
        self.topic_label.setReadOnly(False)

    # --- EVENT HANDLERS ---
    def mousePressEvent(self, e):
        """Clear focus when clicking outside QLineEdit."""
        self.topic_label.clearFocus()
        super().mousePressEvent(e)

    def keyPressEvent(self, e):
        """Toggle topic and timer on spacebar press."""
        if e.key() == Qt.Key.Key_Space:
            self.toggle_timer()
            return

        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.timer_label.hasFocus() or self.topic_label.hasFocus():
                self.centralWidget().setFocus()
                return
            else:
                self.toggle_timer()
                return
            
        super().keyPressEvent(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())