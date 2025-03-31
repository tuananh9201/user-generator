from PyQt5.QtWidgets import QTextEdit
from datetime import datetime


class LogWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setReadOnly(True)
        self.setPlaceholderText("Application logs will appear here...")

    def log(self, message: str):
        """Add a log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.append(f"[{timestamp}] {message}")
