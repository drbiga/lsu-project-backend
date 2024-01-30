from enum import Enum
from typing import List
from abc import ABC, abstractmethod

class SessionPart(Enum):
    WAITING_START = 'WAITING_START'
    READ_COMP = 'READ_COMP'
    HOMEWORK = 'HOMEWORK'
    SURVEY = 'SURVEY'
    FINISHED = 'FINISHED'
