from PyQt5.QtCore import QThread, pyqtSignal
import random
import string
import pandas as pd
from faker import Faker
from datetime import datetime


class UserGeneratorThread(QThread):
    finished = pyqtSignal(bool, str)  # Success status and message
    progress = pyqtSignal(str)  # For logging progress

    def __init__(self, num_users: int, prefix: str, contract: str):
        super().__init__()
        self.num_users = num_users
        self.prefix = prefix
        self.contract = contract
        self.generated_usernames = set()
        self.fake = Faker()

    def run(self):
        try:
            users_data = []
            attempts = 0
            max_attempts = self.num_users * 10

            self.progress.emit(
                f"Starting generation of {self.num_users} users with prefix '{self.prefix}'")

            while len(users_data) < self.num_users and attempts < max_attempts:
                username = self._generate_username()

                if username not in self.generated_usernames:
                    password = self._generate_password()
                    users_data.append(
                        [len(users_data) + 1, username, password])
                    self.generated_usernames.add(username)

                    if len(users_data) % 100 == 0:
                        self.progress.emit(
                            f"Generated {len(users_data)} users...")

                attempts += 1

            if len(users_data) < self.num_users:
                self.finished.emit(
                    False, "Could not generate enough unique usernames. Please try different prefix.")
                return

            filename = self._save_to_excel(users_data)
            self.finished.emit(True, filename)

        except Exception as e:
            self.finished.emit(False, str(e))

    def _generate_username(self) -> str:
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=4))
        random_digits = ''.join(random.choices(string.digits, k=4))
        return f"{self.prefix}_{self.fake.first_name()}_{random_chars}_{random_digits}"

    def _generate_password(self) -> str:
        length = random.randint(8, 20)
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
        return ''.join(random.choice(characters) for _ in range(length))

    def _save_to_excel(self, users_data) -> str:
        df = pd.DataFrame(users_data, columns=['STT', 'Username', 'Password'])
        safe_contract = self.contract.replace("/", "_")
        current_date = datetime.now().strftime('%d-%m-%Y')
        filename = f"{self.num_users}_{current_date}_{safe_contract}.xlsx"
        df.to_excel(filename, index=False)
        return filename
