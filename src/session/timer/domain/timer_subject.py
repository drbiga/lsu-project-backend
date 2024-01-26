import time
from typing import List

from session.timer.domain.timer_observer import TimerObserver


class TimerSubject:
    def __init__(self) -> None:
        self.observers: List[TimerObserver] = []
    
    def set_time(self, minutes: int, seconds: int) -> None:
        self.total = 60*minutes + seconds

    def start(self) -> None:
        while self.total > 0:
            time.sleep(1)
            self.total -= 1
            self.notify()

    def notify(self):
        new_minutes = self.total // 60
        new_seconds = self.total % 60
        for observer in self.observers:
            observer.update(new_minutes, new_seconds)

    def attach(self, observer: TimerObserver) -> None:
        self.observers.append(observer)

    def detach(self, observer: TimerObserver) -> None:
        self.observers.remove(observer)
