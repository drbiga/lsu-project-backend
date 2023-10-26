from fastapi import APIRouter

from student.domain.student_service import StudentService
from student.infra.shelve_students_repository import ShelveStudentsRepository
from session.infra.session_api import session_service

students_router = APIRouter(prefix='/students')
students_repository = ShelveStudentsRepository()
student_service = StudentService(students_repository)

@students_router.get('')
def get_all_student_names():
    return student_service.get_students_names()


@students_router.post('')
def create_student(student_name: str):
    try:
        student_service.create_student(student_name)
        return {
            'status': 'success',
            'message': 'Student created successfully'
        }
    except ValueError:
        return {
            'status': 'err',
            'message': 'Student already exists'
        }

@students_router.post('/{student_name}/start_next_session')
def start_next_session(student_name: str):
    try:
        student_service.start_next_session(session_service, student_name)
        return {
            'status': 'success',
            'message': 'Session started'
        }
    except RuntimeError:
        return {
            'status': 'err',
            'message': 'Session is already running'
        }
    except KeyError:
        return {
            'status': 'err',
            'message': 'Session does not exist yet'
        }

@students_router.get('/{student_name}/next_session_seq_number')
def get_next_session_seq_number(student_name: str):
    try:
        next_seq_number = student_service.get_next_session_seq_number(student_name)
        return {
            'status': 'success',
            'data': next_seq_number
        }
    except AttributeError:
        return {
            'status': 'err',
            'message': 'Student dest not exist'
        }

