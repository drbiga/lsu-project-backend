import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from session.infra.session_api import session_router
from student.infra.shelve_students_repository import ShelveStudentsRepository
from student.domain.student import Student

def main():
    # app = FastAPI()
    # app.add_middleware(CORSMiddleware, allow_methods=['*'], allow_origins=['*'])
    # app.include_router(session_router)
    # uvicorn.run(app, host='0.0.0.0')
    repo = ShelveStudentsRepository()
    s1 = Student(name='Matheus', num_finished_sessions=1)
    repo.save(s1)
    s2 = repo.load('Matheus')


if __name__ == '__main__':
    main()