import time

from typing import List

from threading import Thread

import statistics

from student.domain.student import Student
from student.domain.students_repository import StudentsRepository

from session.domain.session_service import SessionService
from session.domain.session_part import SessionPart

from attention.domain.attention_service import AttentionService
from attention.domain.attention_algorithm import AttentionAlgorithm

MICRO_FEEDBACK_TIME = 1
MACRO_FEEDBACK_TIME_MULTIPLE = 3

class StudentService:
    def __init__(self, repository: StudentsRepository) -> None:
        self.repository = repository
        self.current_student = None

    def create_student(self, student_name: str) -> Student:
        student = Student(name=student_name)
        self.repository.save(student)

    def start_next_session(
        self,
        session_service: SessionService,
        attention_service: AttentionService,
        algo: AttentionAlgorithm,
        student_name: str
    ) -> None:
        self.current_student = self.repository.load(student_name)
        self.current_student.start_new_session()
        session_service.start_session(len(self.current_student.session_executions)+1)
        self.repository.save(self.current_student)
        self.feedback_monitoring_thread = Thread(
            target=lambda: self.__start_recording_feedbacks(attention_service, session_service, algo)
        )
        self.feedback_monitoring_thread.start()

    def get_students_names(self) -> List[str]:
        return self.repository.get_all_student_names()

    def get_next_session_seq_number(self, student_name: str) -> int:
        student = self.repository.load(student_name)
        return len(student.session_executions) + 1

    def __start_recording_feedbacks(
            self,
            attention_service: AttentionService,
            session_service: SessionService,
            attention_algo: AttentionAlgorithm,
        ) -> None:

        session = session_service.executing_session
        micro_sleeps_counter = 0
        micro_feedbacks = []

        while session.part.part == SessionPart.WAITING_START:
            ... # wait

        while not session.part.part == SessionPart.FINISHED:
            time.sleep(MICRO_FEEDBACK_TIME)
            feedback = attention_service.get_attention_feedback(attention_algo)

            # Registering microfeedback for grouping in macro feedback
            micro_feedbacks.append(feedback)
            self.current_student.record_micro_feedback(feedback)
            micro_sleeps_counter += 1
            if micro_sleeps_counter == MACRO_FEEDBACK_TIME_MULTIPLE:
                micro_sleeps_counter = 0
                macro_feedback = round(statistics.mean(micro_feedbacks), 0)
                micro_feedbacks.clear()
                self.current_student.record_macro_feedback(macro_feedback)
        
        # After collecting feedback, save the student with all
        # the session execution history
        self.repository.save(self.current_student)

    def get_student(self, student_name: str) -> Student:
        return self.repository.load(student_name)

    def get_micro_feedback(self, seq_num: int) -> float:
        """Micro feedbacks are calculated using the sequence number.
        The sequence number itself represents the macro feedback for the whole period.
        The index of the microfeedbacks should calculated based on that.
        
        For now, to simplify the code, I'm just going to return the first microfeedback
        for the period.
        """
        return self.current_student.session_executions[-1].micro_feedbacks[MACRO_FEEDBACK_TIME_MULTIPLE*seq_num]

    def get_macro_feedback(self, seq_num: int) -> float:
        return self.current_student.session_executions[-1].macro_feedbacks[seq_num-1]

    def get_attention_feedback(self, seq_num: int) -> float:
        if len(self.current_student.session_executions[-1].macro_feedbacks) < seq_num:
            return self.get_micro_feedback(seq_num)
        else:
            return self.get_macro_feedback(seq_num)


    def get_current_student(self) -> Student:
        return self.current_student
