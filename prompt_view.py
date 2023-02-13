from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PromptView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("<h1>A for Apple<h1>")
        layout.addWidget(label)

        self.setLayout(layout)
