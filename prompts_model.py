import mimetypes
from pathlib import Path

import openpyxl
from PySide6.QtCore import QObject, Signal


class Prompt:
    def __init__(self, id: str, text: str) -> None:
        self.id = id
        self.text = text

    def __repr__(self) -> str:
        return f"Prompt({self.id}, {self.text})"

    def __str__(self) -> str:
        return f"{self.id} {self.text}"


class PromptList(QObject):
    active_prompt_changed = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.prompts: list[Prompt] = []
        self._active_prompt_index = 0

    def __len__(self) -> int:
        return len(self.prompts)

    @property
    def active_prompt_index(self) -> int:
        return self._active_prompt_index

    @active_prompt_index.setter
    def active_prompt_index(self, value: int) -> None:
        if value == self.active_prompt_index or value >= len(self) or value < 0:
            return
        self._active_prompt_index = value
        self.active_prompt_changed.emit(self.active_prompt_index)

    @property
    def active_prompt(self) -> Prompt:
        return self.prompts[self.active_prompt_index]

    def next(self) -> None:
        self.active_prompt_index += 1

    def previous(self) -> None:
        self.active_prompt_index -= 1

    def load_from_path(self, url: str):
        prompts_path = Path(url)
        spreadsheet_mimetypes = [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ]
        if not prompts_path.exists():
            print("Path doesn't exist")
            return
        mime_type = mimetypes.guess_type(prompts_path)[0]
        if mime_type not in spreadsheet_mimetypes:
            raise MimeTypeError()

        workbook = openpyxl.load_workbook(prompts_path, read_only=True)
        sheet = workbook.active

        for row in sheet:
            if len(row) >= 2:
                id, prompt = row[0], row[1]
                print(id.value, prompt.value)
                prompt = Prompt(id.value, prompt.value)
                self.prompts.append(prompt)


class MimeTypeError(Exception):
    pass
