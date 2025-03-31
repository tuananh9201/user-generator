import os
from pathlib import Path
from typing import List, Tuple
import pandas as pd
from datetime import datetime


class FileManager:
    @staticmethod
    def save_users_to_excel(users_data: List, contract: str) -> str:
        df = pd.DataFrame(
            [(user.index, user.username, user.password)
             for user in users_data],
            columns=['STT', 'Username', 'Password']
        )

        safe_contract = contract.replace("/", "_")
        current_date = datetime.now().strftime('%d-%m-%Y')
        filename = f"{len(users_data)}_{current_date}_{safe_contract}.xlsx"
        df.to_excel(filename, index=False)
        return filename

    @staticmethod
    def get_excel_files() -> List[Tuple[str, float]]:
        excel_files = []
        for file in Path().glob('*.xlsx'):
            created_time = file.stat().st_ctime
            excel_files.append((str(file), created_time))

        return sorted(excel_files, key=lambda x: x[1], reverse=True)

    @staticmethod
    def open_file_location(filename: str) -> None:
        abs_path = Path(filename).absolute()
        if os.name == 'nt':  # Windows
            os.system(f'explorer /select,"{abs_path}"')
        else:  # macOS and Linux
            os.system(f'open -R "{abs_path}"')
