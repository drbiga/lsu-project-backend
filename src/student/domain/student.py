from pydantic import BaseModel

class Student(BaseModel):
    name: str
    num_finished_sessions: int

    def finish_one_more_session(self) -> None:
        self.num_finished_sessions += 1