from fastapi import APIRouter

from session.infra.instances import session_service
from session.timer.infra.websocket_timer import timer_websocket_router
from session.infra.websocket_session_part_observer import session_part_router

session_router = APIRouter(prefix='/sessions')
session_router.include_router(timer_websocket_router)
session_router.include_router(session_part_router)

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
