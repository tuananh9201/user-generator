import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from gui.widgets.input_form import InputForm
from gui.widgets.files_table import FilesTable
from gui.widgets.log_widget import LogWidget
from core.user_generator import UserGeneratorThread


class UserGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        version = "1.0.1"
        self.setWindowTitle(f"User Generator v{version}")
        self.setWindowIcon(QIcon("resources/app_icon.ico"))
        self.setGeometry(100, 100, 1200, 600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create splitter for main layout
        main_splitter = QSplitter(Qt.Horizontal)

        # Left box
        left_box = QWidget()
        left_layout = QVBoxLayout(left_box)

        # Input form
        self.input_form = InputForm()
        self.input_form.generate_btn.clicked.connect(self.generate_users)

        left_layout.addWidget(self.input_form)

        # Files table
        self.files_table = FilesTable()
        self.files_table.itemDoubleClicked.connect(self.open_file_location)
        left_layout.addWidget(self.files_table)

        left_box.setLayout(left_layout)

        # Set minimum width for left box
        left_box.setMinimumWidth(250)  # Prevents it from becoming too small

        # Right box - Logs
        self.log_widget = LogWidget()

        # Add widgets to splitter
        main_splitter.addWidget(left_box)
        main_splitter.addWidget(self.log_widget)

        # Set the left box to take 1/3 of the space, right box to take 2/3
        main_splitter.setStretchFactor(0, 1)  # Left box (1 part)
        main_splitter.setStretchFactor(1, 2)  # Right box (2 parts)

        # Add splitter to main layout
        layout.addWidget(main_splitter)

        self.log_widget.log("Application started")

    def generate_users(self):
        try:
            values = self.input_form.get_values()
            num_users = int(values['num_users'])
            prefix = values['prefix']
            contract = values['contract']

            if not all([num_users, prefix, contract]):
                self.log_widget.log("Error: All fields must be filled")
                return

            self.input_form.generate_btn.setEnabled(False)
            self.input_form.generate_btn.setText("Generating...")

            self.generator_thread = UserGeneratorThread(
                num_users, prefix, contract)
            self.generator_thread.progress.connect(self.log_widget.log)
            self.generator_thread.finished.connect(self.generation_completed)
            self.generator_thread.start()

        except ValueError:
            self.log_widget.log("Error: Invalid number of users")
            self.input_form.generate_btn.setEnabled(True)
            self.input_form.generate_btn.setText("Generate Users")

    def generation_completed(self, success: bool, message: str):
        self.input_form.generate_btn.setEnabled(True)
        self.input_form.generate_btn.setText("Generate Users")

        if success:
            self.log_widget.log(
                f"Successfully generated users and saved to '{message}'")
            self.files_table.update_files()
        else:
            self.log_widget.log(f"Error: {message}")
            QMessageBox.warning(self, "Warning", message)

    def open_file_location(self, item):
        if item.column() == 0:
            filename = item.text()
            abs_path = os.path.abspath(filename)
            self.log_widget.log(f"Opening file location: {abs_path}")
            os.system(
                f'explorer /select,"{abs_path}"' if os.name == 'nt' else f'open -R "{abs_path}"')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/app_icon.ico"))
    window = UserGeneratorApp()
    window.show()
    sys.exit(app.exec_())
