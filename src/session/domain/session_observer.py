from abc import ABC, abstractmethod


class SessionObserver(ABC):
    @abstractmethod
    def update(self, session_data: dict) -> None:
        ...
