from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title='taskflow')

app.include_router(auth.router)


@app.get('/')
def read_root() -> dict:
    return { "message": "Welcome to taskflow!"}
