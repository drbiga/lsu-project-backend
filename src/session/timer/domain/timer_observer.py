from abc import ABC, abstractmethod

class TimerObserver(ABC):
    @abstractmethod
    def update(self, new_time_minutes: int, new_time_seconds: int) -> None:
        ...
