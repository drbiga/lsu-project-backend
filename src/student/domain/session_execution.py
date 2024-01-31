from pydantic import BaseModel
from typing import List, Optional

from attention.domain.attention import Attention

class SessionExecution(BaseModel):
    seq_num: int
    macro_feedbacks: Optional[List[float]] = []
    micro_feedbacks: Optional[List[float]] = []
    second_wise_data: Optional[List[Attention]] = []

    def record_macro_feedback(self, feedback: float) -> None:
        self.macro_feedbacks.append(feedback)
    
    def record_micro_feedback(self, feedback: float) -> None:
        self.micro_feedbacks.append(feedback)

    def record_second_wise_data(self, attention: Attention) -> None:
        self.second_wise_data.append(attention)
