from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (QFileDialog, QFrame, QLabel, QPushButton,
                               QVBoxLayout)


class OpenView(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        open_button = QPushButton("Open")
        open_button.setDefault(True)

        drop_label = QLabel("<b>Drag and drop<b>")
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        or_label = QLabel("or")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(drop_label)
        layout.addWidget(or_label)
        layout.addWidget(open_button)
        layout.addStretch()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(layout)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setContentsMargins(10, 10, 10, 10)

        open_button.clicked.connect(self.open_file_dialog)

    @Slot()
    def open_file_dialog(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setMimeTypeFilters(
            [
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/octet-stream",
            ],
        )
        if dialog.exec():
            urls = dialog.selectedFiles()
            print(urls)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if len(urls) > 1:
            print("Can only accept single file")
            return
        url = urls[0].path()
        print(url)
