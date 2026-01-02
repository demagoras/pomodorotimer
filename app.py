from datetime import timedelta
import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget
)

class MainWindow(QMainWindow):
    """
    Main application window for the Pomodoro Timer.
    Handles the UI layout and countdown logic.
    """
    def __init__(self):
        super().__init__()

        self.WORK_TIME = timedelta(seconds = 3)
        self.WORK_TOPIC = "Science"
        self.TICK_INTERVAL = 1000 # milliseconds

        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(300, 200)

        self.topic_label = QLabel(self.WORK_TOPIC)
        self.topic_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
            )
        self.topic_label.setStyleSheet("font-size: 24px;")

        self.timer_label = QLabel()
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setContentsMargins(0, 0, 0, 30)
        self.timer_label.setStyleSheet("font-size: 48px;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.toggle_time_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")
        self.toggle_time_button.clicked.connect(self.toggle_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        filename_time_over = "sounds/bell.wav"
        self.time_over_sound = QSoundEffect(self)
        self.time_over_sound.setSource(QUrl.fromLocalFile(filename_time_over))
        # Could check whether the sound loaded correctly for certain cases
        # Although the C++ engine does it automatically
        # if self.time_over_sound.status() == QSoundEffect.Status.Error
        #    print(f"Error loading sound: {filename_time_over}")

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
        """Resets the timer, UI, and clock rhythm."""
        self.timer.stop()
        self.time_over_sound.stop()

        self.remaining_time = self.WORK_TIME
        self.update_label_text()
        self.topic_label.setText(self.WORK_TOPIC)
        self.toggle_time_button.setText("Pause")
        self.toggle_time_button.setEnabled(True)
        self.timer.start(self.TICK_INTERVAL)

    # --- UI HELPERS ---
    def update_timer(self):
        """Update the timer display every second."""
        if self.remaining_time.total_seconds() > 0:
            self.remaining_time -= timedelta(milliseconds=self.TICK_INTERVAL)
            self.update_label_text()
        else:
            self.timer.stop()

            self.topic_label.setText("Break time!")
            self.timer_label.setText("00:00")

            self.time_over_sound.setLoopCount(1) # Play sound only once
            self.time_over_sound.play()
            
            self.toggle_time_button.setEnabled(False)

    def update_label_text(self):
        """Handles the format MM:SS or H:MM:SS for the timer label."""
        total_seconds = int(self.remaining_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        mins, secs = divmod(remainder, 60)
        
        if self.remaining_time >= timedelta(hours=1):
            self.timer_label.setText(f"{hours}:{mins:02d}:{secs:02d}")
        else:
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())