from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from session.infra.session_api import session_router
from student.infra.students_api import students_router
from attention.infra.attention_api import attention_router


def main():
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_methods=['*'], allow_origins=['*'])
    app.include_router(session_router, tags=['sessions'])
    app.include_router(students_router, tags=['students'])
    app.include_router(attention_router, tags=['attention'])
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()