import time

from session.infra.session import session_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

def main():
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_methods=['*'], allow_origins=['*'])
    app.include_router(session_router)
    uvicorn.run(app, host='0.0.0.0')


if __name__ == '__main__':
    main()