from pydantic import BaseModel
from typing import List, Optional

from student.domain.session_execution import SessionExecution

class Student(BaseModel):
    name: str
    session_executions: Optional[List[SessionExecution]] = []

    def start_new_session(self) -> None:
        new_execution = SessionExecution(seq_num=len(self.session_executions)+1)
        self.session_executions.append(new_execution)

    def record_macro_feedback(self, feedback: int) -> None:
        # Recording is always done to the last executing session
        self.session_executions[-1].record_macro_feedback(feedback)

    def record_micro_feedback(self, feedback: int) -> None:
        # Recording is always done to the last executing session
        self.session_executions[-1].record_micro_feedback(feedback)
