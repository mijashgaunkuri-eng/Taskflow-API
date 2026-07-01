# TaskFlow

TaskFlow is a minimal FastAPI project scaffold for task management with a modern async backend setup.

## What is included so far

- FastAPI application entrypoint
- Centralized settings handling with pydantic-settings
- Async SQLAlchemy database configuration
- Initial User model
- Alembic migration support

## Project structure

- `app/core/` — configuration and database setup
- `app/crud/` — CRUD logic
- `app/models/` — SQLAlchemy models
- `app/routers/` — API routes
- `app/schemas/` — request/response schemas
- `app/dependencies.py` — shared dependencies
- `app/main.py` — application entrypoint

## Requirements

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the project root with values such as:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/taskflow
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Run the app

```bash
uvicorn app.main:app --reload
```

## Database migrations

Initialize or update migrations with Alembic:

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
