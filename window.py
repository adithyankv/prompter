from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from open_view import OpenView
from prompt_view import PromptView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("App")
        self.resize(250, 250)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.open_view = OpenView()
        self.prompt_view = PromptView()

        self.stack.addWidget(self.open_view)
        self.stack.addWidget(self.prompt_view)

    @Slot()
    def change_views(self) -> None:
        self.stack.setCurrentWidget(self.prompt_view)
