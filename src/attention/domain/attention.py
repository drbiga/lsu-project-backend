from pydantic import BaseModel
from datetime import datetime


class Attention(BaseModel):
    timestamp_start: datetime
    timestamp_end: datetime
    num_keyboard_strokes: int
    num_mouse_clicks: int
    size_mouse_scroll: int
    dist_mouse_movement: float
