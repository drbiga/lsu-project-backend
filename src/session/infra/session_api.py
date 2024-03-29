from pydantic import BaseModel
from fastapi import APIRouter, WebSocket, Response, status

from session.domain.session_service import SessionHasNotStartedError
from session.infra.instances import session_service
from session.infra.websocket_session_observer import WebSocketSessionObserver

session_router = APIRouter(prefix='/sessions')

SESSION_NOT_STARTED_ERR_TYPE = 'SESSION_NOT_STARTED'

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
            'status': 'success',
            'is_passthrough': session_service.get_session(session_seq_number).is_passthrough
        }
    except:
        return {
            'status': 'err',
            'is_passthrough': 0
        }

@session_router.get('/executing', status_code=status.HTTP_200_OK)
def get_executing_session(response: Response) -> dict:
    try:
        return {
            'status': 'success',
            'session_data': session_service.get_executing_session()
        }
    except SessionHasNotStartedError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'status': 'err',
            'err_type': SESSION_NOT_STARTED_ERR_TYPE,
            'message': e.message
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'status': 'err',
            'message': str(e)
        }

@session_router.post('/executing/resume', status_code=status.HTTP_200_OK)
def resume_executing_session(response: Response) -> dict:
    try:
        session_service.resume_ongoing_session()
        return {
            'status': 'success',
            'message': 'Session resumed'
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'status': 'err',
            'message': str(e)
        }

@session_router.websocket('/ws')
async def attach_session_observer(websocket: WebSocket):
    await websocket.accept()
    observer = WebSocketSessionObserver(websocket)
    session_service.attach_session_observer(observer)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        print('Error in websocket connection')

