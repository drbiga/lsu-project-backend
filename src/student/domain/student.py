from pydantic import BaseModel
from typing import List, Optional

from student.domain.session_execution import SessionExecution
from attention.domain.attention import Attention

class Student(BaseModel):
    name: str
    session_executions: Optional[List[SessionExecution]] = []
    survey_queue_link: Optional[str] = None


    def start_new_session(self) -> None:
        new_execution = SessionExecution(seq_num=len(self.session_executions)+1)
        self.session_executions.append(new_execution)

    def record_macro_feedback(self, feedback: int) -> None:
        # Recording is always done to the last executing session
        self.session_executions[-1].record_macro_feedback(feedback)

    def record_micro_feedback(self, feedback: int) -> None:
        # Recording is always done to the last executing session
        self.session_executions[-1].record_micro_feedback(feedback)

    def record_raw_attention_data(self, attention_data: Attention) -> None:
        # Recording is always done to the last executing session
        self.session_executions[-1].record_raw_attention_data(attention_data)

    def set_survey_queue_link(self, link: str) -> None:
        self.survey_queue_link = link
