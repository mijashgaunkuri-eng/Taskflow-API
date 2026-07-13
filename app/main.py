from fastapi import FastAPI
from app.routers import auth, task

app = FastAPI(title='taskflow')

app.include_router(auth.router)
app.include_router(task.router)


@app.get('/')
def read_root() -> dict:
    return { "message": "Welcome to taskflow!"}
