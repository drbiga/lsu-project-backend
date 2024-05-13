import time

from threading import Thread

from session.domain.session import Session
from session.domain.session_observer import SessionObserver
from session.domain.sessions_repository import SessionsRepository
from session.domain.session_part import SessionPart

SESSION_STATE_RESET_TIME_CHECK = 60


class SessionHasNotStartedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "You have not started the session yet"

class SessionService:
    def __init__(self, repository: SessionsRepository) -> None:
        self.repository = repository
        # Session can have two states from the session service perspective
        # It can be either:
        # - Running
        # - Finished
        # If the session is finished, we set the executing session to None
        # to let the user start a new one
        self.executing_session = None

    def create_session(self, seq_number: int, read_comp_link: str, survey_link: str, is_passthrough: bool) -> None:
        session = Session(seq_number=seq_number, read_comp_link=read_comp_link, survey_link=survey_link, is_passthrough=is_passthrough)
        self.repository.save(session)

    def get_session(self, seq_number: int) -> Session:
        session = self.repository.load(seq_number)
        return session

    def start_session(self, seq_number: int) -> None:
        if self.executing_session is not None:
            if self.executing_session.session_part != SessionPart.FINISHED.value:
                raise RuntimeError('Only one session is allowed to run each time')
        
        self.executing_session = self.repository.load(seq_number)
        self.session_worker = Thread(target=lambda: self.run_session_worker())
        self.session_worker.start()

    def run_session_worker(self):
        self.executing_session.start() # this will also run in a separate thread

        while not self.executing_session.session_part == SessionPart.FINISHED:
            # Wait a minute, literally
            time.sleep(SESSION_STATE_RESET_TIME_CHECK)
        
        # Reset the state so that the user can start a new session even
        # if they do not close the backend on the laptop
        self.executing_session = None


    def resume_ongoing_session(self) -> None:
        """Resumes the on-going session for the student after he/she has
        pressed the Continue button upon submitting the Read-Comp survey
        """
        if not self.executing_session.has_resumed:
            if self.executing_session.timer_is_running:
                self.executing_session.stop_timer()
            session_worker = Thread(target=lambda: self.executing_session.enter_homework())
            session_worker.start()

    def attach_session_observer(self, observer: SessionObserver) -> None:
        self.executing_session.attach(observer)

    def get_timer_value(self) -> int:
        return self.executing_session.timer

    def get_session_part(self) -> str:
        return self.executing_session.session_part

    def get_executing_session(self) -> dict:
        if self.executing_session is None:
            raise SessionHasNotStartedError()
        return self.executing_session.get_data()
