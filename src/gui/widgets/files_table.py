from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from datetime import datetime
import os

class FilesTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["File Name", "Generated Time"])
        self.update_files()

    def update_files(self):
        self.setRowCount(0)
        excel_files = []
        
        for f in os.listdir('.'):
            if f.endswith('.xlsx'):
                file_info = os.stat(f)
                created_time = file_info.st_ctime
                excel_files.append((f, created_time))

        excel_files.sort(key=lambda x: x[1], reverse=True)

        for file, created_timestamp in excel_files:
            created_time = datetime.fromtimestamp(
                created_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            row_position = self.rowCount()
            self.insertRow(row_position)

            self.setItem(row_position, 0, QTableWidgetItem(file))
            self.setItem(row_position, 1, QTableWidgetItem(created_time))

        self.resizeColumnsToContents()