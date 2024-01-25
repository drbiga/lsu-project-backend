import shelve
from typing import List
from student.domain.student import Student

from student.domain.students_repository import StudentsRepository


class ShelveStudentsRepository(StudentsRepository):
    def save(self, student: Student) -> None:
        with shelve.open('data/students.shelve') as students:
            students[student.name] = student.model_dump()

    def load(self, student_name: str) -> Student:
        with shelve.open('data/students.shelve') as students:
            student = students[student_name]
        
        return Student(**student)

    def get_all_student_names(self) -> List[str]:
        with shelve.open('data/students.shelve') as students:
            student_names = list(students.keys())
        
        return student_names
