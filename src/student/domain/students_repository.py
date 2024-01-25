from abc import ABC, abstractmethod
from typing import List

from student.domain.student import Student


class StudentsRepository(ABC):
    @abstractmethod
    def save(self, student: Student) -> None:
        ...

    @abstractmethod
    def load(self, student_name: str) -> Student:
        ...

    @abstractmethod
    def get_all_student_names(self) -> List[str]:
        ...
