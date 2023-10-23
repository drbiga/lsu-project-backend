import shelve

from session.domain.session import Session
from session.domain.sessions_repository import SessionsRepository

class ShelveSessionsRepository(SessionsRepository):
    def save(self, session: Session) -> None:
        with shelve.open('sessions.shelve') as sessions:
            sessions[str(session.seq_number)] = session.json()

    def load(self, seq_number: str) -> Session:
        with shelve.open('sessions.shelve') as sessions:
            session = sessions[str(seq_number)]
        
        return Session(**session)
    
