from typing import Optional, Callable

import time
from threading import Timer
from pydantic import BaseModel

from session.domain.session_part import SessionPart, SessionPartSubject
from session.timer.domain.timer_subject import TimerSubject

class Session:
    def __init__(self, seq_number: int, read_comp_link: str, survey_link: str, is_passthrough: bool) -> None:
        self.seq_number = seq_number
        self.read_comp_link = read_comp_link
        self.survey_link = survey_link
        self.is_passthrough = is_passthrough

        self.part: SessionPartSubject = SessionPartSubject()
        self.part.set_part(SessionPart.WAITING_START)
        self.timer = TimerSubject()

    def start(self) -> None:
        # Wait until both part and timer observers have connected
        while len(self.part.observers) == 0 or len(self.timer.observers) == 0:
            ...
        # Wait just a little longer just to be sure that session part observer
        # is up and running on the client side
        time.sleep(1)
        self.part.set_part(SessionPart.READ_COMP)
        self.timer.start(0, 5)
        self.enter_homework()

    def enter_homework(self) -> None:
        self.part.set_part(SessionPart.HOMEWORK)
        self.timer.start(0, 5)
        self.enter_survey()
    
    def enter_survey(self) -> None:
        self.part.set_part(SessionPart.SURVEY)
        self.timer.start(0, 5)
        self.finish()

    def finish(self) -> None:
        self.part.set_part(SessionPart.FINISHED)

    def json(self):
        return {
            'seq_number': self.seq_number,
            'read_comp_link': self.read_comp_link,
            'survey_link': self.survey_link,
            'is_passthrough': self.is_passthrough
        }

    def __repr__(self) -> str:
        return '\n'.join([
            'Session',
            f'Current part: {self.part}',
            f'Remaining time: {self.get_remaining_time()}'
        ])
