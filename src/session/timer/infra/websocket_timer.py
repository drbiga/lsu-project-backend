import asyncio
from fastapi import APIRouter, WebSocket

from session.timer.domain.timer_observer import TimerObserver
# from session.timer.domain.timer_subject import TimerSubject
from session.infra.instances import session_service

timer_websocket_router = APIRouter(prefix='/timer')

@timer_websocket_router.websocket('/ws')
async def attach_timer_observer(websocket: WebSocket):
    await websocket.accept()
    observer = WebSocketTimerObserver(websocket)
    session_service.attach_timer_observer(observer)
    # subject = TimerSubject(0, 10)
    # subject.attach(observer)
    # subject.start()
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        print('Error in websocket connection')

class WebSocketTimerObserver(TimerObserver):
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket

    def update(self, new_time_minutes: int, new_time_seconds: int) -> None:
        asyncio.run(self.websocket.send_json({
            'minutes': new_time_minutes,
            'seconds': new_time_seconds
        }))