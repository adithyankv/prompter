from enum import Enum, auto
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class RecordStopButton(QPushButton):
    def __init__(self) -> None:
        super().__init__()
        self.state = ButtonState.RECORD

        self.record_icon = QIcon()
        self.record_icon.addFile("resources/record.svg")
        self.stop_icon = QIcon()
        self.stop_icon.addFile("resources/stop.svg")

        self.clicked.connect(self.toggle_state)
        self.update_icon()

    def update_icon(self) -> None:
        if self.state == ButtonState.RECORD:
            self.setIcon(self.record_icon)
        else:
            self.setIcon(self.stop_icon)

    @Slot()
    def toggle_state(self) -> None:
        if self.state == ButtonState.RECORD:
            self.state = ButtonState.STOP
        else:
            self.state = ButtonState.RECORD
        self.update_icon()


class ButtonState(Enum):
    RECORD = auto()
    STOP = auto()
