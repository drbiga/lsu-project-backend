from session.domain.session import Session
from session.domain.sessions_repository import SessionsRepository
from session.domain.session_part import SessionPart

class SessionService:
    def __init__(self, repository: SessionsRepository) -> None:
        self.repository = repository
        self.executing_session = None

    def create_session(self, seq_number: int, read_comp_link: str, survey_link: str) -> None:
        session = Session(seq_number=seq_number, read_comp_link=read_comp_link, survey_link=survey_link)
        self.repository.save(session)

    def get_session(self, seq_number: int) -> Session:
        session = self.repository.load(seq_number)
        return session

    def start_session(self, seq_number: int) -> None:
        if self.executing_session is not None:
            raise RuntimeError('Only one session is allowed to run each time')
        
        self.executing_session = self.repository.load(seq_number)
        self.executing_session.start()

    def get_current_session_part(self) -> SessionPart:
        return self.executing_session.part