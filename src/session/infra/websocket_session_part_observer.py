import asyncio
from fastapi import APIRouter, WebSocket
from concurrent.futures import ThreadPoolExecutor

from session.domain.session_part import SessionPart, SessionPartObserver
from session.infra.instances import session_service
from async_lock import async_lock

session_part_router = APIRouter(prefix='/session_part')

@session_part_router.websocket('/ws')
async def attach_timer_observer(websocket: WebSocket):
    await websocket.accept()
    observer = WebSocketSessionPartObserver(websocket)
    session_service.attach_session_part_observer(observer)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        print('Error in websocket connection')

class WebSocketSessionPartObserver(SessionPartObserver):
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket

    def update(self, new_session_part: SessionPart) -> None:
        with async_lock:
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(
                    lambda: asyncio.run(self.websocket.send_json({
                        'session_part': new_session_part.value
                    }))
                )
