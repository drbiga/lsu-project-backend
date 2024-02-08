from threading import Thread

from session.domain.session import Session
from session.domain.session_observer import SessionObserver
from session.domain.sessions_repository import SessionsRepository
from session.domain.session_part import SessionPart


class SessionService:
    def __init__(self, repository: SessionsRepository) -> None:
        self.repository = repository
        self.executing_session = None

    def create_session(self, seq_number: int, read_comp_link: str, survey_link: str, is_passthrough: bool) -> None:
        session = Session(seq_number=seq_number, read_comp_link=read_comp_link, survey_link=survey_link, is_passthrough=is_passthrough)
        self.repository.save(session)

    def get_session(self, seq_number: int) -> Session:
        session = self.repository.load(seq_number)
        return session

    def start_session(self, seq_number: int) -> None:
        if self.executing_session is not None:
            if self.executing_session.session_part != SessionPart.FINISHED:
                raise RuntimeError('Only one session is allowed to run each time')
        
        self.executing_session = self.repository.load(seq_number)
        Thread(target=lambda: self.executing_session.start()).start()

    def resume_ongoing_session(self) -> None:
        """Resumes the on-going session for the student after he/she has
        pressed the Continue button upon submitting the Read-Comp survey
        """
        if not self.executing_session.has_resumed:
            session_worker = Thread(target=lambda: self.executing_session.enter_homework())
            session_worker.start()

    def attach_session_observer(self, observer: SessionObserver) -> None:
        self.executing_session.attach(observer)

    def get_timer_value(self) -> int:
        return self.executing_session.timer

    def get_session_part(self) -> str:
        return self.executing_session.session_part

    def get_executing_session(self) -> dict:
        return self.executing_session.get_data()
