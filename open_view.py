from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout


class OpenView(QFrame):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        self.open_button = QPushButton("Open")
        self.open_button.setDefault(True)

        drop_label = QLabel("<b>Drag and drop<b>")
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        or_label = QLabel("or")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(drop_label)
        layout.addWidget(or_label)
        layout.addWidget(self.open_button)
        layout.addStretch()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(layout)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setContentsMargins(10, 10, 10, 10)
