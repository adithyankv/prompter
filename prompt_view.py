import html
from pathlib import Path
from typing import Optional

from pydub import AudioSegment
from pydub.playback import play
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QWidget)

from prompts_model import PromptList
from timestamp_logger import TimestampLogger


class PromptView(QWidget):
    recording_state_changed = Signal()

    def __init__(self, prompts: PromptList) -> None:
        super().__init__()
        self._is_recording = False
        self.prompts = prompts
        self.recording_session_started = False
        self.timestamp_logger = TimestampLogger()

        self.create_layout()
        self.update_ui()

        self.next_button.clicked.connect(self.next_prompt)
        self.prev_button.clicked.connect(self.prev_prompt)
        self.record_stop_button.clicked.connect(self.on_record_button_clicked)
        self.finish_button.clicked.connect(self.on_finish_button_clicked)
        self.redo_button.clicked.connect(self.on_redo_button_clicked)
        self.index_entry.textChanged.connect(self.on_index_entry_changed)

        self.prompts.active_prompt_changed.connect(self.on_prompt_changed)
        self.recording_state_changed.connect(self.update_ui)

    def create_layout(self) -> None:
        self.prompt_label = QLabel()
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Prev")
        self.finish_button = QPushButton("Finish")
        root_path = Path(__file__).parent

        self.redo_button = QPushButton()
        redo_icon = QIcon()
        redo_icon_path = Path(root_path, "resources/icons/repeat.svg")
        redo_icon.addFile(str(redo_icon_path.absolute()))
        self.redo_button.setIcon(redo_icon)

        self.record_stop_button = QPushButton()
        self.record_icon = QIcon()
        record_icon_path = Path(root_path, "resources/icons/record.svg")
        self.record_icon.addFile(str(record_icon_path))
        self.stop_icon = QIcon()
        stop_icon_path = Path(root_path, "resources/icons/stop.svg")
        self.stop_icon.addFile(str(stop_icon_path))
        self.record_stop_button.setIcon(self.record_icon)

        index_box = QHBoxLayout()
        self.index_entry = QLineEdit()
        self.total_indices_label = QLabel(f"/{len(self.prompts)}")
        index_validator = QIntValidator(0, len(self.prompts))
        self.index_entry.setValidator(index_validator)

        index_box.addWidget(self.index_entry)
        index_box.addWidget(self.total_indices_label)
        index_box.addStretch()

        self.next_button.setToolTip("Next prompt")
        self.prev_button.setToolTip("Previous prompt")
        self.redo_button.setToolTip("Redo")
        self.finish_button.setToolTip("Finish recording")

        self.prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prompt_label.setWordWrap(True)

        buttons_box = QHBoxLayout()
        finish_box = QHBoxLayout()
        layout = QVBoxLayout()

        buttons_box.addWidget(self.record_stop_button)
        buttons_box.addWidget(self.prev_button)
        buttons_box.addWidget(self.next_button)
        buttons_box.addWidget(self.redo_button)

        finish_box.addWidget(self.finish_button)
        finish_box.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addStretch()
        layout.addWidget(self.prompt_label)
        layout.addLayout(buttons_box)
        layout.addLayout(index_box)
        layout.addStretch()

        layout.addLayout(finish_box)
        self.setLayout(layout)

    @Slot()
    def on_record_button_clicked(self) -> None:
        if not self.recording_session_started:
            self.recording_session_started = True
            self.timestamp_logger.start_logging()

        if not self.is_recording:
            self.timestamp_logger.active_prompt = self.prompts.active_prompt
            # cue should be played before logging timestamp to avoid cue being
            # part of recording
            self.play_cue()
            self.timestamp_logger.log_start()
        else:
            # cue should be played after logging timestamp to avoid cue being
            # part of recording
            self.timestamp_logger.log_end()

        self.toggle_recording_state()

    @Slot()
    def on_finish_button_clicked(self) -> None:
        self.timestamp_logger.finish_logging()
        filename = self.run_save_dialog()
        if filename:
            save_file_path = f"{filename}.json"
            print(save_file_path)
            self.timestamp_logger.save_to_file(save_file_path)

    def run_save_dialog(self) -> Optional[str]:
        save_dialog = QFileDialog()
        save_dialog.setFileMode(QFileDialog.AnyFile)
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if save_dialog.exec():
            output_file_name = save_dialog.selectedFiles()[0]
            return output_file_name
        return None

    @Slot()
    def on_redo_button_clicked(self) -> None:
        self.timestamp_logger.remove_log(self.prompts.active_prompt)
        self.update_ui()

    def play_cue(self) -> None:
        root_path = Path(__file__).parent
        cue_path = Path(root_path, "resources", "sounds", "beep.wav")
        cue = AudioSegment.from_wav(str(cue_path))
        play(cue)

    @Slot()
    def update_ui(self) -> None:
        self.update_prompt()
        self.update_buttons()
        self.update_index()

    @Slot()
    def on_prompt_changed(self) -> None:
        self.timestamp_logger.active_prompt = self.prompts.active_prompt
        self.update_ui()

    def update_prompt(self) -> None:
        self.prompt_label.setText(
            f"<h1>{html.escape(self.prompts.active_prompt.text)}<h1>"
        )

    def update_index(self) -> None:
        self.index_entry.setText(str(self.prompts.active_prompt_index))

    def update_buttons(self) -> None:
        self.finish_button.setDisabled(self.is_recording)
        self.redo_button.setDisabled(self.is_recording)

        is_last_prompt = self.prompts.active_prompt_index == len(self.prompts) - 1
        is_first_prompt = self.prompts.active_prompt_index == 0
        self.next_button.setDisabled(self.is_recording or is_last_prompt)
        self.prev_button.setDisabled(self.is_recording or is_first_prompt)

        is_logged = self.prompts.active_prompt in self.timestamp_logger.logged_prompts
        self.record_stop_button.setDisabled(is_logged)
        self.redo_button.setDisabled(not is_logged)

        if self.is_recording:
            self.record_stop_button.setToolTip("Stop")
            self.record_stop_button.setIcon(self.stop_icon)
        else:
            self.record_stop_button.setToolTip("Record")
            self.record_stop_button.setIcon(self.record_icon)

    @Slot()
    def on_index_entry_changed(self) -> None:
        entry = self.index_entry.text()
        if entry:
            self.prompts.active_prompt_index = int(entry)

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    @is_recording.setter
    def is_recording(self, value: bool):
        if value == self._is_recording:
            return
        self._is_recording = value
        self.recording_state_changed.emit()

    @Slot()
    def toggle_recording_state(self) -> None:
        self.is_recording = not self.is_recording

    @Slot()
    def next_prompt(self) -> None:
        self.prompts.next()

    @Slot()
    def prev_prompt(self) -> None:
        self.prompts.previous()
