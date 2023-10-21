from fastapi import APIRouter

from session.domain.session import Session

session_router = APIRouter(prefix='/session')

session: Session = Session()

@session_router.post('')
def create_session():
    global session
    
    session = Session()
    return {
        'status': 'success',
        'message': 'Session created successfully'
    }


@session_router.post('/start')
def start_session():
    global session

    if session is None:
        return {
            'status': 'err',
            'message': 'Session not created yet'
        }

    session.start()

@session_router.get('/part')
def get_current_part():
    global session

    if session is None:
        return {
            'status': 'err',
            'message': 'Session not created yet'
        }

    return {
        'status': 'success',
        'data': session.part
    }


@session_router.get('/remaining_time')
def get_remaining_time():
    global session

    if session is None:
        return {
            'status': 'err',
            'message': 'Session not created yet'
        }

    return {
        'status': 'success',
        'data': session.get_remaining_time()
    }
