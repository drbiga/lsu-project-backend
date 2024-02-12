import time

from typing import List

from session.domain.session_part import SessionPart
from session.domain.session_observer import SessionObserver

class Session:
    TIME_SECONDS_READ_COMP = 10 * 60
    TIME_SECONDS_HOMEWORK = 40 * 60
    TIME_SECONDS_SURVEY = 10 * 60

    def __init__(self, seq_number: int, read_comp_link: str, survey_link: str, is_passthrough: bool) -> None:
        # Subject attributes (observable)
        self.observers: List[SessionObserver] = []

        # Session attributes
        self.seq_number = seq_number
        self.read_comp_link = read_comp_link
        self.survey_link = survey_link
        self.is_passthrough = is_passthrough

        # State variable to prevent session from being resumed multiple times
        # regardless of how many times the user press the resume button
        # Could prevent bugs where they press the button multiple times and have
        # multiple homework/post-session survey times.
        self.has_resumed = False

        self.session_part = SessionPart.WAITING_START.value
        self.timer = Session.TIME_SECONDS_READ_COMP

    # ---------------------------------------------------------------------------------
    # Subject methods
    def attach(self, observer: SessionObserver) -> None:
        self.observers.append(observer)

    def detach(self, observer: SessionObserver) -> SessionObserver:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update({
                'session_part': self.session_part,
                'remaining_time': self.timer
            })

    # ---------------------------------------------------------------------------------
    # Domain methods
    def run_timer(self) -> None:
        # At every timer tick, we emit an update to the observersf
        while self.timer > 0:
            self.timer -= 1
            self.notify()
            time.sleep(1)

    def start(self) -> None:
        # Wait until observer has attached (web application)
        while len(self.observers) == 0:
            time.sleep(1)

        # Wait just a little longer just to be sure that session part observer
        # is up and running on the client side
        time.sleep(1)
        self.session_part = SessionPart.READ_COMP.value
        self.run_timer()
        # self.enter_homework()

    def enter_homework(self) -> None:
        # Once the session has entered the homework part, it is
        # considered as resumed, and the user cannot resume it
        # once again
        self.has_resumed = True
        self.session_part = SessionPart.HOMEWORK.value
        self.timer = Session.TIME_SECONDS_HOMEWORK
        self.run_timer()
        self.enter_survey()
    
    def enter_survey(self) -> None:
        self.session_part = SessionPart.SURVEY.value
        self.timer = Session.TIME_SECONDS_SURVEY
        self.run_timer()
        self.finish()

    def finish(self) -> None:
        self.session_part = SessionPart.FINISHED.value
        self.notify()

    def json(self):
        return {
            'seq_number': self.seq_number,
            'read_comp_link': self.read_comp_link,
            'survey_link': self.survey_link,
            'is_passthrough': self.is_passthrough,
        }
    
    def get_data(self) -> dict:
        return {
            'session_part': self.session_part,
            'remaining_time': self.timer
        }

    def __repr__(self) -> str:
        return '\n'.join([
            'Session',
            f'Current part: {self.session_part}',
            f'Remaining time: {self.timer}'
        ])
