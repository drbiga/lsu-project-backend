import asyncio
from fastapi import WebSocket
from concurrent.futures import ThreadPoolExecutor

from session.domain.session_observer import SessionObserver
from async_lock import async_lock

class WebSocketSessionObserver(SessionObserver):
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket

    def update(self, session_part: str, total_time_left: float) -> None:
        with async_lock:
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(
                    lambda: asyncio.run(self.websocket.send_json({
                        'session_part': session_part,
                        'total_time_left': total_time_left
                    }))
                )
