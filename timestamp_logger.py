import time

from prompts_model import Prompt


class TimestampLogger:
    def __init__(self) -> None:
        self.timestamps: dict[str, dict] = dict()
        self.active_prompt: Prompt
        self.logged_prompts: set[Prompt] = set()

    def start_logging(self) -> None:
        self.session_start_time = time.time()

    def log_start(self) -> None:
        self.active_prompt_recording_start = time.time()

    def log_end(self) -> None:
        self.active_prompt_recording_end = time.time()
        start_time = self.active_prompt_recording_start - self.session_start_time
        end_time = self.active_prompt_recording_end - self.session_start_time
        self.timestamps[self.active_prompt.id] = {
            "start": round(start_time, 3),
            "end": round(end_time, 3),
            "start_timestamp": self.format_timestamp(start_time),
            "end_timestamp": self.format_timestamp(end_time),
        }
        self.logged_prompts.add(self.active_prompt)

    def remove_log(self, prompt: Prompt) -> None:
        del self.timestamps[self.active_prompt.id]
        self.logged_prompts.remove(prompt)

    def finish_logging(self) -> None:
        print(self.timestamps)

    def format_timestamp(self, time: float) -> str:
        minutes, seconds = int(time // 60), time % 60
        hours, minutes = int(minutes // 60), minutes % 60
        milliseconds, seconds = seconds % 1, int(seconds // 1)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{int(milliseconds*1000):03d}"
