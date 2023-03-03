import sys
import traceback

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from open_view import OpenView
from prompt_view import PromptView
from prompts_model import MimeTypeError, PromptList


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("App")
        self.resize(250, 250)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.open_view = OpenView()

        self.open_view.file_selected.connect(self.load_prompts)

        self.stack.addWidget(self.open_view)

    @Slot()
    def load_prompts(self, url: str) -> None:
        prompts = PromptList()
        prompts.load_from_path(url)

        self.prompt_view = PromptView(prompts)
        self.prompt_view.logging_finished.connect(self.on_logging_finished)

        self.stack.addWidget(self.prompt_view)
        self.stack.setCurrentWidget(self.prompt_view)

    @Slot()
    def on_logging_finished(self) -> None:
        self.stack.setCurrentWidget(self.open_view)
