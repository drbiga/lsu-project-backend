import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from session.infra.session_api import session_router
from student.infra.students_api import students_router
# from student.infra.shelve_students_repository import ShelveStudentsRepository
# from student.domain.student import Student

def main():
    # repo = ShelveStudentsRepository()

    # s1 = Student(name='Matheus', num_finished_sessions=1)
    # repo.save(s1)
    # s2 = repo.load('Matheus')

    # print(repo.get_all_student_names())

    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_methods=['*'], allow_origins=['*'])
    app.include_router(session_router)
    app.include_router(students_router)
    uvicorn.run(app, host='0.0.0.0')


if __name__ == '__main__':
    main()