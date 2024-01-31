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

MICRO_FEEDBACK_TIME = 60 # one micro feedback every minute
MACRO_FEEDBACK_TIME_MULTIPLE = 3 # one macro feedback every three minutes

TOTAL_FEEDBACKS = 20

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
        print("Starting session", len(self.current_student.session_executions))
        session_service.start_session(len(self.current_student.session_executions))
        self.repository.save(self.current_student)

        self.feedback_monitoring_thread = Thread(
            target=lambda: self.__start_recording_feedbacks(attention_service, session_service, algo)
        )
        self.feedback_monitoring_thread.start()

        self.attention_monitoring_thread = Thread(
            target=lambda: self.__start_recording_second_wise_data(attention_service, session_service)
        )
        self.attention_monitoring_thread.start()

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

        while session.session_part == SessionPart.WAITING_START:
            time.sleep(0.5)

        while not session.session_part == SessionPart.FINISHED:
            time.sleep(MICRO_FEEDBACK_TIME)
            feedback = attention_service.get_attention_feedback(attention_algo)
            feedback = int(feedback)

            # Registering microfeedback for grouping in macro feedback
            micro_feedbacks.append(feedback)
            self.current_student.record_micro_feedback(feedback)
            micro_sleeps_counter += 1
            if micro_sleeps_counter == MACRO_FEEDBACK_TIME_MULTIPLE:
                micro_sleeps_counter = 0
                macro_feedback = int(round(statistics.mean(micro_feedbacks), 0))
                micro_feedbacks.clear()
                self.current_student.record_macro_feedback(macro_feedback)
        
        # After collecting feedback, save the student with all
        # the session execution history
        self.repository.save(self.current_student)

    def __start_recording_second_wise_data(
            self,
            attention_service: AttentionService,
            session_service: SessionService,
        ) -> None:
        # For every second
        # Get raw values from somewhere
        # Save values into session execution
        session = session_service.executing_session

        # Waiting for the user to actually start the session        
        while session.session_part == SessionPart.WAITING_START:
            time.sleep(0.5)

        while not session.session_part == SessionPart.FINISHED:
            time.sleep(1)
            attention = attention_service.get_current_attention()
            self.current_student.record_second_wise_data(attention)

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
        return self.current_student.session_executions[-1].macro_feedbacks[seq_num]

    def get_attention_feedbacks(self) -> List[int]:
        feedbacks = []
        for i in range(TOTAL_FEEDBACKS):
            # Behaviour that we want:
            # When we have the "macro" feedback for some period, use the macro feedback
            # If we don't have the macro feedback for some specific period, then
            #   If we have any micro feedback, use it
            #   Else, use the error code (-1)
            if i < len(self.current_student.session_executions[-1].macro_feedbacks):
                feedbacks.append(self.get_macro_feedback(i))
            else:
                len_micro_feedbacks = len(self.current_student.session_executions[-1].micro_feedbacks)
                if MACRO_FEEDBACK_TIME_MULTIPLE*i < len_micro_feedbacks:
                    feedbacks.append(self.get_micro_feedback(i))
                else:
                    feedbacks.append(-1)
        return feedbacks


    def get_current_student(self) -> Student:
        return self.current_student
