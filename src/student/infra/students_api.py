from fastapi import APIRouter

from student.domain.student_service import StudentService
from student.infra.shelve_students_repository import ShelveStudentsRepository

from session.infra.session_api import session_service
from attention.infra.instances import attention_service, attention_algorithm

students_router = APIRouter(prefix='/students')
students_repository = ShelveStudentsRepository()
student_service = StudentService(students_repository)

@students_router.get('')
def get_all_student_names():
    return student_service.get_students_names()

@students_router.get('/{student_name}')
def get_student(student_name: str) -> dict:
    return student_service.get_student(student_name).model_dump()


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
        student_service.start_next_session(session_service, attention_service, attention_algorithm, student_name)
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

@students_router.get('/current/session_executions/last')
def get_last_session_executions() -> dict:
    return student_service.current_student.session_executions[-1].model_dump()


@students_router.get('/current/attention_feedback')
def get_attention_feedback(seq_num: int) -> float:
    return student_service.get_attention_feedback(seq_num)


@students_router.get('/current/data')
def get_current_student():
    s = student_service.get_current_student()
    return {
        'status': 'ok' if s is not None else 'err',
        'student': None if s is None else s.model_dump()
    }
