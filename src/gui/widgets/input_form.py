from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)


class InputForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Number of users
        self.num_users = self._create_input_field(
            "Số lượng users:", "Số lượng users")

        # Prefix
        self.prefix = self._create_input_field("Prefix:", "Prefix")

        # Contract
        self.contract = self._create_input_field(
            "Số hợp đồng:", "06102023-01/VDC")

        # Generate button
        self.generate_btn = QPushButton("Generate Users")
        layout.addWidget(self.generate_btn)

    def _create_input_field(self, label: str, placeholder: str) -> QLineEdit:
        container = QWidget()
        layout = QHBoxLayout(container)

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)

        layout.addWidget(QLabel(label))
        layout.addWidget(input_field)

        self.layout().addWidget(container)
        return input_field

    def get_values(self):
        return {
            'num_users': self.num_users.text(),
            'prefix': self.prefix.text(),
            'contract': self.contract.text()
        }
