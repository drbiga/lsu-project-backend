from typing import Optional, Callable

import time
from threading import Timer
from pydantic import BaseModel

from session.domain.session_part import SessionPart
from session.timer.domain.timer_subject import TimerSubject

class Session:
    def __init__(self, seq_number: int, read_comp_link: str, survey_link: str) -> None:
        self.seq_number = seq_number
        self.read_comp_link = read_comp_link
        self.survey_link = survey_link

        self.part: SessionPart = SessionPart.WAITING_START
        self.timer = None

    def start(self) -> None:
        self.part = SessionPart.READ_COMP
        # self.wait_and_proceed(lambda: self.enter_homework(), seconds=10)
        self.timer = TimerSubject()
        self.timer.start(0, 10)
        self.enter_homework()

    def enter_homework(self) -> None:
        self.part = SessionPart.HOMEWORK
        # self.wait_and_proceed(lambda: self.enter_survey(), seconds=40)
        self.timer.start(0, 40)
        self.enter_survey()
    
    def enter_survey(self) -> None:
        self.part = SessionPart.SURVEY
        # self.wait_and_proceed(lambda: self.finish(), seconds=10)
        self.timer.start(0, 10)
        self.finish()

    def finish(self) -> None:
        self.part = SessionPart.FINISHED

    # def wait_and_proceed(self, set_next_state: Callable, minutes: Optional[int] = None, seconds: Optional[int] = None):
    #     if minutes is None and seconds is None:
    #         raise ValueError('You must pass at least one time unit to the wait_for() function')

    #     total = 0
    #     if minutes is not None:
    #         total += 60* minutes
    #     if seconds is not None:
    #         total += seconds

    #     self.timer = Timer(total, set_next_state)
    #     self.timer.start_time = time.time()
    #     self.timer.start()

    def get_remaining_time(self):
        # Shared variable. Not gonna use a lock, because it is read-only
        if self.timer is not None:
            remaining_time = self.timer.interval - int(time.time() - self.timer.start_time)
            if remaining_time >= 0:
                return remaining_time
        return 0

    def json(self):
        return {
            'seq_number': self.seq_number,
            'read_comp_link': self.read_comp_link,
            'survey_link': self.survey_link
        }

    def __repr__(self) -> str:
        return '\n'.join([
            'Session',
            f'Current part: {self.part}',
            f'Remaining time: {self.get_remaining_time()}'
        ])
