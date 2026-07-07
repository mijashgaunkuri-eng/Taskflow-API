# TaskFlow

TaskFlow is a minimal FastAPI project scaffold for task management with an async backend setup.

## What is included so far

- FastAPI application entrypoint
- Centralized settings handling with pydantic-settings
- Async SQLAlchemy database configuration
- User model and basic user creation flow
- Password hashing with pwdlib
- Alembic migration support
- Docker Compose configuration for PostgreSQL

## Project structure

- `app/core/` — configuration, database setup, and security helpers
- `app/crud/` — CRUD logic
- `app/models/` — SQLAlchemy models
- `app/routers/` — API routes
- `app/schemas/` — request/response schemas
- `app/dependencies.py` — shared dependencies
- `app/main.py` — application entrypoint
- `alembic/` — migration scripts
- `docker-compose.yml` — local PostgreSQL setup

## Requirements

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the project root using the example below:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/taskflow
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

You can copy the example file:

```bash
copy .env.example .env
```

## Run the app

Start the database with Docker Compose:

```bash
docker-compose up -d postgres
```

Then start the API:

```bash
uvicorn app.main:app --reload
```

## Database migrations

Create or apply migrations with Alembic:

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

## GitHub upload

This repository is ready to be pushed to GitHub. Make sure your local environment file remains private and is not committed.

