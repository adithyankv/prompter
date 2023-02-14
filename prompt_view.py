from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                               QWidget)

from prompts_model import PromptList
from record_stop_button import RecordStopButton
from redo_button import RedoButton


class PromptView(QWidget):
    def __init__(self, prompts: PromptList) -> None:
        super().__init__()

        self.prompts = prompts
        self.prompt_label = QLabel()
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Prev")
        self.record_stop_button = RecordStopButton()
        self.redo_button = RedoButton()
        self.finish_button = QPushButton("Finish")
        buttons_box = QHBoxLayout()
        buttons_box.addWidget(self.record_stop_button)
        buttons_box.addWidget(self.prev_button)
        buttons_box.addWidget(self.next_button)
        buttons_box.addWidget(self.redo_button)

        self.update_prompt()
        self.prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.prompt_label)
        layout.addLayout(buttons_box)
        layout.addStretch()

        finish_box = QHBoxLayout()
        finish_box.addWidget(self.finish_button)
        finish_box.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(finish_box)

        self.next_button.clicked.connect(self.next_prompt)
        self.prev_button.clicked.connect(self.prev_prompt)
        self.prompts.active_prompt_changed.connect(self.update_prompt)
        self.prompts.active_prompt_changed.connect(self.update_nav_buttons)

        self.setLayout(layout)
        self.update_nav_buttons()

    def update_prompt(self) -> None:
        self.prompt_label.setText(f"<h1>{self.prompts.active_prompt.text}<h1>")

    def update_nav_buttons(self) -> None:
        if self.prompts.active_prompt_index == len(self.prompts) - 1:
            self.next_button.setDisabled(True)
        else:
            self.next_button.setEnabled(True)
        if self.prompts.active_prompt_index == 0:
            self.prev_button.setDisabled(True)
        else:
            self.prev_button.setEnabled(True)

    @Slot()
    def next_prompt(self) -> None:
        self.prompts.next()

    @Slot()
    def prev_prompt(self) -> None:
        self.prompts.previous()
