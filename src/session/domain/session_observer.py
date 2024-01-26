from abc import ABC, abstractmethod


class SessionObserver(ABC):
    @abstractmethod
    def update(self, session_part: str, total_time_left: float) -> None:
        ...
