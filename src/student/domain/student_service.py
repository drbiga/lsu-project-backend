from typing import List

from student.domain.student import Student
from student.domain.students_repository import StudentsRepository
from session.domain.session_service import SessionService


class StudentService:
    def __init__(self, repository: StudentsRepository) -> None:
        self.repository = repository

    def create_student(self, student_name: str) -> Student:
        student = Student(name=student_name, num_finished_sessions=0)
        self.repository.save(student)

    def start_next_session(self, session_service: SessionService, student_name: str) -> None:
        student = self.repository.load(student_name)
        session_service.start_session(student.num_finished_sessions+1)
        student.finish_one_more_session()
        self.repository.save(student)

    def get_students_names(self) -> List[str]:
        return self.repository.get_all_student_names()
