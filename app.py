import logging
import sys
import traceback

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from window import MainWindow


def main():
    app = QApplication()

    window = MainWindow()
    window.show()

    sys.excepthook = on_exception

    app.exec()


def on_exception(exception_type, exception_value, exception_traceback):
    error_dialog = QMessageBox()
    error_message = "".join(traceback.format_tb(exception_traceback))
    logging.error(f"{exception_value}\n{error_message}")
    error_dialog.setWindowModality(Qt.ApplicationModal)
    error_dialog.setWindowTitle("Oops, something went wrong!")
    error_dialog.setText(str(exception_value))
    error_dialog.setDetailedText(error_message)
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.exec()


if __name__ == "__main__":
    main()
