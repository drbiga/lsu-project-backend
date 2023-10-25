from enum import Enum
from typing import List
from abc import ABC, abstractmethod

class SessionPart(Enum):
    WAITING_START = 'WAITING_START'
    READ_COMP = 'READ_COMP'
    HOMEWORK = 'HOMEWORK'
    SURVEY = 'SURVEY'
    FINISHED = 'FINISHED'


class SessionPartObserver(ABC):
    @abstractmethod
    def update(self, new_session_part: SessionPart) -> None:
        ...


class SessionPartSubject:
    def __init__(self) -> None:
        self.part = SessionPart.WAITING_START
        self.observers: List[SessionPartObserver] = []

    def set_part(self, new_session_part: SessionPart) -> None:
        self.part = new_session_part
        self.notify()

    def notify(self):
        for observer in self.observers:
            observer.update(self.part)

    def attach(self, observer: SessionPartObserver) -> None:
        self.observers.append(observer)

    def detach(self, observer: SessionPartObserver) -> None:
        self.observers.remove(observer)

