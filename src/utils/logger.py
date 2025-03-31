import logging
from datetime import datetime
from typing import Optional
from PyQt5.QtWidgets import QTextEdit

class QtLogger:
    def __init__(self, log_widget: Optional[QTextEdit] = None):
        self.log_widget = log_widget
        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger('UserGenerator')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message: str, level: str = 'info'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        
        if self.log_widget:
            self.log_widget.append(log_message)
        
        getattr(self.logger, level)(message)