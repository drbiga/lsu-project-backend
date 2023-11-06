import time
import random

from threading import Thread

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from session.infra.session_api import session_router
from student.infra.students_api import students_router
from attention.infra.attention_api import attention_router

from session.timer.infra.cli_timer import CLITimer
from session.timer.domain.timer_subject import TimerSubject

# from student.infra.shelve_students_repository import ShelveStudentsRepository
# from student.domain.student import Student

def write_test_feedback_file():
    while True:
        time.sleep(1)
        with open('feedback.txt', 'w') as out:
            out.write(str(random.randint(1, 3)))

def main():
    # repo = ShelveStudentsRepository()

    # s1 = Student(name='Matheus', num_finished_sessions=1)
    # repo.save(s1)
    # s2 = repo.load('Matheus')

    # print(repo.get_all_student_names())

    # timer = TimerSubject(0, 10)
    # observer = CLITimer()
    # timer.attach(observer)
    # timer.start()

    t = Thread(target=write_test_feedback_file)
    t.start()

    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_methods=['*'], allow_origins=['*'])
    app.include_router(session_router, tags=['sessions'])
    app.include_router(students_router, tags=['students'])
    app.include_router(attention_router, tags=['attention'])
    uvicorn.run(app, host='0.0.0.0')


if __name__ == '__main__':
    main()