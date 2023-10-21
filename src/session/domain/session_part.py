from enum import Enum

class SessionPart(Enum):
    WAITING_START = 'WAITING_START'
    READ_COMP = 'READ_COMP'
    HOMEWORK = 'HOMEWORK'
    SURVEY = 'SURVEY'
    FINISHED = 'FINISHED'
