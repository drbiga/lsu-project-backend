from fastapi import APIRouter

from session.infra.instances import session_service
from session.timer.infra.websocket_timer import timer_websocket_router

session_router = APIRouter(prefix='/sessions')
session_router.include_router(timer_websocket_router)

@session_router.post('')
def create_session(seq_number: int, read_comp_link: str, survey_link: str):
    session_service.create_session(seq_number, read_comp_link, survey_link)
    return {
        'status': 'success',
        'message': 'Session created successfully'
    }


@session_router.post('/start')
def start_session(seq_number: int):
    try:
        session_service.start_session(seq_number)
        return {
            'status': 'success',
            'message': 'Session started successfully'
        }
    except KeyError:
        return {
            'status': 'err',
            'message': 'Session does not exist yet'
        }

@session_router.get('')
def get_session(seq_number: int):
    return session_service.get_session(seq_number)

@session_router.get('/part')
def get_current_part():
    try:
        part = session_service.get_current_session_part()
        return {
            'status': 'success',
            'data': part.value
        }
    except AttributeError:
        return {
            'status': 'err',
            'message': 'Session not started yet'
        }


@session_router.get('/remaining_time')
def get_remaining_time():
    try:
        remaining_time = session_service.get_current_session_remaining_time_seconds()
        return {
            'status': 'success',
            'data': remaining_time
        }
    except AttributeError:
        return {
            'status': 'err',
            'message': 'Session not started yet'
        }
