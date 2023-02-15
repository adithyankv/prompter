from enum import Enum, auto

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class RedoButton(QPushButton):
    def __init__(self) -> None:
        super().__init__()

        redo_icon = QIcon()
        redo_icon.addFile("resources/icons/repeat.svg")
        self.setIcon(redo_icon)
