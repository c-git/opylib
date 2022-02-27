from datetime import datetime

from opylib.log import log


class StopWatch:
    def __init__(self, name, *, should_log_end=False, start_log_level=None):
        self.start_time = datetime.now()
        self.name = name
        self.end_time = None
        self.should_log_end = should_log_end
        self.run_msg = "Still Running"
        log(f"{self.name} stop watch start time: {self.start_time}",
            start_log_level)

    def end(self):
        self.end_time = datetime.now()
        self.run_msg = f"{self.name} stop watch runtime was {self.runtime()}"
        if self.should_log_end:
            log(f"{self.name} stop watch end time: {self.end_time}")
        log(self.run_msg)

    def runtime(self):
        return self.end_time - self.start_time

    def as_float(self):
        return self.runtime().total_seconds()
