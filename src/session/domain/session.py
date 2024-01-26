import time

from typing import List

from session.domain.session_part import SessionPart, SessionPartSubject
from session.timer.domain.timer_subject import TimerSubject
from session.domain.session_observer import SessionObserver

class Session:    
    def __init__(self, seq_number: int, read_comp_link: str, survey_link: str, is_passthrough: bool) -> None:
        # Subject attributes (observable)
        self.observers: List[SessionObserver] = []

        # Session attributes
        self.seq_number = seq_number
        self.read_comp_link = read_comp_link
        self.survey_link = survey_link
        self.is_passthrough = is_passthrough

        self.part: SessionPartSubject = SessionPartSubject()
        self.part.set_part(SessionPart.WAITING_START)
        self.timer = TimerSubject()

    # ---------------------------------------------------------------------------------
    # Subject methods
    def attach(self, observer: SessionObserver) -> None:
        self.observers.append(observer)

    def detach(self, observer: SessionObserver) -> SessionObserver:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self.part.part.value, self.timer.total)

    # ---------------------------------------------------------------------------------
    # Domain methods
    def start(self) -> None:
        # Wait until either
        # - Both part and timer observers have connected
        # - The session observer has connected
        part_and_timer_observers = len(self.part.observers) > 0 and len(self.timer.observers) > 0
        session_observer = len(self.observers) > 0
        exit_condition = part_and_timer_observers or session_observer
        while not exit_condition:
            part_and_timer_observers = len(self.part.observers) > 0 and len(self.timer.observers) > 0
            session_observer = len(self.observers) > 0
            exit_condition = part_and_timer_observers or session_observer

        print('Exited the wait while loop')
        # Wait just a little longer just to be sure that session part observer
        # is up and running on the client side
        time.sleep(1)
        self.part.set_part(SessionPart.READ_COMP)
        self.timer.set_time(10, 0)
        self.notify()
        self.timer.start()
        self.enter_homework()

    def enter_homework(self) -> None:
        self.part.set_part(SessionPart.HOMEWORK)
        self.timer.set_time(40, 0)
        self.notify()
        self.timer.start()
        self.enter_survey()
    
    def enter_survey(self) -> None:
        self.part.set_part(SessionPart.SURVEY)
        self.timer.set_time(10, 0)
        self.notify()
        self.timer.start()
        self.finish()

    def finish(self) -> None:
        self.part.set_part(SessionPart.FINISHED)
        self.notify()

    def json(self):
        return {
            'seq_number': self.seq_number,
            'read_comp_link': self.read_comp_link,
            'survey_link': self.survey_link,
            'is_passthrough': self.is_passthrough,
            'session_part': self.part.part.value,
            'total_time_left': self.timer.total
        }

    def __repr__(self) -> str:
        return '\n'.join([
            'Session',
            f'Current part: {self.part}',
            f'Remaining time: {self.get_remaining_time()}'
        ])
