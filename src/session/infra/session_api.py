from pydantic import BaseModel
from fastapi import APIRouter

from session.infra.instances import session_service
from session.timer.infra.websocket_timer import timer_websocket_router
from session.infra.websocket_session_part_observer import session_part_router

session_router = APIRouter(prefix='/sessions')
session_router.include_router(timer_websocket_router)
session_router.include_router(session_part_router)

class CreateSessionRequest(BaseModel):
    seq_number: int
    read_comp_link: str
    survey_link: str
    is_passthrough: bool

@session_router.post('')
def create_session(seq_number: int, read_comp_link: str, survey_link: str, is_passthrough: bool):
    session_service.create_session(seq_number, read_comp_link, survey_link, is_passthrough)
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

@session_router.get('/timer_value')
def get_timer_value():
    try:
        timer_value = session_service.get_timer_value()
        return {
            'status': 'success',
            'data': timer_value
        }
    except AttributeError:
        return {
            'status': 'err',
            'message': 'Session does not exist yet'
        }

@session_router.get('/session_part')
def get_session_part():
    try:
        part = session_service.get_session_part()
        return {
            'status': 'success',
            'data': part
        }
    except AttributeError:
        return {
            'status': 'err',
            'message': 'Session does not exist yet'
        }


@session_router.get('/{session_seq_number}/is_passthrough')
def check_session_is_passthrough(session_seq_number: int) -> dict:
    try:
        return {
            'status': 'ok',
            'is_passthrough': session_service.get_session(session_seq_number).is_passthrough
        }
    except:
        return {
            'status': 'err',
            'is_passthrough': False
        }
