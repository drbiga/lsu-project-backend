from pydantic import BaseModel
from typing import List, Optional

class SessionExecution(BaseModel):
    seq_num: int
    macro_feedbacks: Optional[List[float]] = []
    micro_feedbacks: Optional[List[float]] = []

    def record_macro_feedback(self, feedback: float) -> None:
        self.macro_feedbacks.append(feedback)
    
    def record_micro_feedback(self, feedback: float) -> None:
        self.micro_feedbacks.append(feedback)
