import random
import string
from typing import List, Tuple
from dataclasses import dataclass
from faker import Faker
from ..utils.constants import (
    MAX_ATTEMPTS_MULTIPLIER,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_CHARS
)

@dataclass
class UserData:
    username: str
    password: str
    index: int

class UserGenerator:
    def __init__(self, prefix: str, num_users: int):
        self.prefix = prefix
        self.num_users = num_users
        self.fake = Faker()
        self.generated_usernames = set()

    def generate_users(self) -> List[UserData]:
        users_data = []
        attempts = 0
        max_attempts = self.num_users * MAX_ATTEMPTS_MULTIPLIER

        while len(users_data) < self.num_users and attempts < max_attempts:
            username = self._generate_username()
            
            if username not in self.generated_usernames:
                password = self._generate_password()
                user = UserData(
                    username=username,
                    password=password,
                    index=len(users_data) + 1
                )
                users_data.append(user)
                self.generated_usernames.add(username)

            attempts += 1

        if len(users_data) < self.num_users:
            raise ValueError("Could not generate enough unique usernames")

        return users_data

    def _generate_username(self) -> str:
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=4))
        random_digits = ''.join(random.choices(string.digits, k=4))
        random_name = self.fake.first_name()
        return f"{self.prefix}_{random_name}_{random_chars}_{random_digits}"

    def _generate_password(self) -> str:
        length = random.randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
        return ''.join(random.choice(PASSWORD_CHARS) for _ in range(length))