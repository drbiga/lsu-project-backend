from abc import ABC, abstractmethod

from session.domain.session import Session


class SessionsRepository(ABC):
    @abstractmethod
    def save(self, session: Session) -> None:
        ...


    @abstractmethod
    def load(self, seq_number: str) -> Session:
        ...
