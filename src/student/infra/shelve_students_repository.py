import shelve
from student.domain.student import Student

from student.domain.students_repository import StudentsRepository


class ShelveStudentsRepository(StudentsRepository):
    def save(self, student: Student) -> None:
        with shelve.open('students.shelve') as students:
            students[student.name] = student.model_dump()

    def load(self, student_name: str) -> Student:
        with shelve.open('students.shelve') as students:
            student = students[student_name]
        
        return Student(**student)
