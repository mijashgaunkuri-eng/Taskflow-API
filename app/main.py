from fastapi import FastAPI
from app.routers import example
from app.core.config import settings

app = FastAPI(title='taskflow')

app.include_router(example.router)


@app.get('/')
def read_root() -> dict:
    return {"database_url": settings.database_url}
