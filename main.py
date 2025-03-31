import sys
import os
import random
import string
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QTextEdit, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon


class UserGeneratorThread(QThread):
    finished = pyqtSignal(bool, str)  # Success status and message
    progress = pyqtSignal(str)  # For logging progress

    def __init__(self, num_users, prefix, contract):
        super().__init__()
        self.num_users = num_users
        self.prefix = prefix
        self.contract = contract
        self.generated_usernames = set()

    def run(self):
        try:
            users_data = []
            attempts = 0
            max_attempts = self.num_users * 10

            self.progress.emit(
                f"Starting generation of {self.num_users} users with prefix '{self.prefix}'")

            while len(users_data) < self.num_users and attempts < max_attempts:
                random_chars = ''.join(
                    random.choices(string.ascii_lowercase, k=4))
                random_digits = ''.join(random.choices(string.digits, k=4))
                username = f"{self.prefix}_{self.generate_random_name()}_{random_chars}_{random_digits}"

                if username not in self.generated_usernames:
                    password = self.generate_random_password()
                    users_data.append(
                        [len(users_data) + 1, username, password])
                    self.generated_usernames.add(username)

                    # Emit progress every 100 users
                    if len(users_data) % 100 == 0:
                        self.progress.emit(
                            f"Generated {len(users_data)} users...")

                attempts += 1

            if len(users_data) < self.num_users:
                self.finished.emit(
                    False, "Could not generate enough unique usernames. Please try different prefix.")
                return

            # Create DataFrame and save to Excel
            df = pd.DataFrame(users_data, columns=[
                              'STT', 'Username', 'Password'])
            safe_contract = self.contract.replace("/", "_")
            filename = f"{self.num_users}_{safe_contract}.xlsx"
            df.to_excel(filename, index=False)

            self.finished.emit(True, filename)

        except Exception as e:
            self.finished.emit(False, str(e))

    def generate_random_name(self):
        from faker import Faker
        fake = Faker()
        return fake.first_name()

    def generate_random_password(self):
        length = random.randint(8, 20)
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
        return ''.join(random.choice(characters) for _ in range(length))


class UserGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        version = "1.0.0"
        self.setWindowTitle(f"User Generator v{version}")
        # Set application icon
        self.setWindowIcon(QIcon("resources/app_icon.ico"))
        # Made window wider for split view
        self.setGeometry(100, 100, 1200, 600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create splitter for main layout
        main_splitter = QSplitter(Qt.Horizontal)

        # Left box (Box 1) - Contains inputs and table
        left_box = QWidget()
        left_layout = QVBoxLayout(left_box)

        # Group 1 - Input fields and button (Vertical Layout)
        input_group = QWidget()
        input_layout = QVBoxLayout(input_group)

        # Number of users
        users_container = QWidget()
        users_layout = QHBoxLayout(users_container)
        self.num_users = QLineEdit()
        self.num_users.setPlaceholderText("Số lượng users")
        users_layout.addWidget(QLabel("Số lượng users:"))
        users_layout.addWidget(self.num_users)
        input_layout.addWidget(users_container)

        # Prefix
        prefix_container = QWidget()
        prefix_layout = QHBoxLayout(prefix_container)
        self.prefix = QLineEdit()
        self.prefix.setPlaceholderText("Prefix")
        prefix_layout.addWidget(QLabel("Prefix:"))
        prefix_layout.addWidget(self.prefix)
        input_layout.addWidget(prefix_container)

        # Contract name
        contract_container = QWidget()
        contract_layout = QHBoxLayout(contract_container)
        self.contract = QLineEdit()
        self.contract.setPlaceholderText("06102023-01/VDC")
        contract_layout.addWidget(QLabel("Số hợp đồng:"))
        contract_layout.addWidget(self.contract)
        input_layout.addWidget(contract_container)

        # Generate button
        self.generate_btn = QPushButton("Generate Users")
        self.generate_btn.clicked.connect(self.generate_users)
        input_layout.addWidget(self.generate_btn)

        # Add input group to left layout
        left_layout.addWidget(input_group)

        # Create table for files
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(2)
        self.files_table.setHorizontalHeaderLabels(
            ["File Name", "Generated Time"])
        self.files_table.itemDoubleClicked.connect(self.open_file_location)
        left_layout.addWidget(self.files_table)

        # Right box (Box 2) - Contains logs
        right_box = QWidget()
        right_layout = QVBoxLayout(right_box)

        # Create logs box
        self.logs_box = QTextEdit()
        self.logs_box.setReadOnly(True)
        self.logs_box.setPlaceholderText(
            "Application logs will appear here...")
        right_layout.addWidget(self.logs_box)

        # Add boxes to main splitter
        main_splitter.addWidget(left_box)
        main_splitter.addWidget(right_box)

        # Set initial sizes for splitter (60% left, 40% right)
        main_splitter.setSizes([720, 480])

        # Add splitter to main layout
        layout.addWidget(main_splitter)

        # Load existing files
        self.update_files_table()
        self.log("Application started")

    def log(self, message):
        """Add a log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logs_box.append(f"[{timestamp}] {message}")

    def generate_random_name(self):
        # Using faker for more realistic and varied names
        from faker import Faker
        fake = Faker()
        return fake.first_name()

    def generate_random_password(self):
        length = random.randint(8, 20)
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_users(self):
        try:
            num_users = int(self.num_users.text())
            prefix = self.prefix.text()
            contract = self.contract.text()

            if not all([num_users, prefix, contract]):
                self.log("Error: All fields must be filled")
                return

            # Disable the generate button while processing
            self.generate_btn.setEnabled(False)
            self.generate_btn.setText("Generating...")

            # Create and start the generator thread
            self.generator_thread = UserGeneratorThread(
                num_users, prefix, contract)
            self.generator_thread.progress.connect(self.log)
            self.generator_thread.finished.connect(self.generation_completed)
            self.generator_thread.start()

        except ValueError:
            self.log("Error: Invalid number of users")
            self.generate_btn.setEnabled(True)
            self.generate_btn.setText("Generate Users")

    def generation_completed(self, success, message):
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate Users")

        if success:
            self.log(f"Successfully generated users and saved to '{message}'")
            self.update_files_table()
        else:
            self.log(f"Error: {message}")
            QMessageBox.warning(self, "Warning", message)

    def update_files_table(self):
        self.files_table.setRowCount(0)

        # Get all Excel files with their creation times
        excel_files = []
        for f in os.listdir('.'):
            if f.endswith('.xlsx'):
                file_info = os.stat(f)
                created_time = file_info.st_ctime
                excel_files.append((f, created_time))

        # Sort files by creation time (newest first)
        excel_files.sort(key=lambda x: x[1], reverse=True)

        self.log(f"Found {len(excel_files)} Excel files in directory")

        for file, created_timestamp in excel_files:
            created_time = datetime.fromtimestamp(
                created_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            row_position = self.files_table.rowCount()
            self.files_table.insertRow(row_position)

            self.files_table.setItem(row_position, 0, QTableWidgetItem(file))
            self.files_table.setItem(
                row_position, 1, QTableWidgetItem(created_time))

        self.files_table.resizeColumnsToContents()

    def open_file_location(self, item):
        if item.column() == 0:  # Only respond to clicks in the filename column
            filename = item.text()
            abs_path = os.path.abspath(filename)
            self.log(f"Opening file location: {abs_path}")
            os.system(
                f'explorer /select,"{abs_path}"' if os.name == 'nt' else f'open -R "{abs_path}"')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Set application-wide icon
    app.setWindowIcon(QIcon("resources/app_icon.ico"))
    window = UserGeneratorApp()
    window.show()
    sys.exit(app.exec_())
