# TaskFlow

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138.1-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.51-red.svg)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791.svg)](https://www.postgresql.org/)

TaskFlow is a RESTful task-management API built with FastAPI and PostgreSQL. It provides user registration, JWT-based authentication, and per-user CRUD operations for tasks with status tracking. The backend is fully asynchronous—SQLAlchemy 2.x async sessions, `asyncpg` as the database driver, and Alembic for schema migrations.

---

## Features

- **Async FastAPI application** — Non-blocking request handling with Uvicorn ASGI server and automatic OpenAPI documentation at `/docs` and `/redoc`.
- **User authentication** — Registration with unique username and email validation; login via OAuth2 password flow; JWT access tokens signed with HS256.
- **Password security** — Argon2 hashing through `pwdlib` (recommended configuration); plaintext passwords are never stored.
- **Task management** — Create, list, retrieve, update, and delete tasks scoped to the authenticated user.
- **Task status workflow** — Three states: `pending`, `in_progress`, and `completed`; filterable via query parameter on list endpoints.
- **Pagination** — Task listing supports `skip` and `limit` query parameters (default limit: 10).
- **Centralized configuration** — Environment-driven settings via `pydantic-settings` loaded from a `.env` file.
- **Database migrations** — Alembic with async migration support; initial schema creates `users` and `tasks` tables with foreign-key relationships and cascade delete.
- **Local development database** — Docker Compose service for PostgreSQL 17 with persistent volume storage.

---

## Technologies Used

| Category | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ (uses `str \| None` union syntax) |
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) | 0.138.1 |
| ASGI server | [Uvicorn](https://www.uvicorn.org/) | 0.49.0 |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0.51 |
| Database driver | [asyncpg](https://github.com/MagicStack/asyncpg) | 0.31.0 |
| Migrations | [Alembic](https://alembic.sqlalchemy.org/) | 1.18.5 |
| Validation / settings | [Pydantic](https://docs.pydantic.dev/), [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | 2.13.4 / 2.14.2 |
| Password hashing | [pwdlib](https://github.com/frankie567/pwdlib) (Argon2) | 0.2.1 |
| JWT | [python-jose](https://github.com/mpdavis/python-jose) | *(used in code; install separately)* |
| Database | PostgreSQL | 17 (via Docker) |
| Containerization | Docker Compose | — |
| Environment loading | python-dotenv | 1.2.2 |

> **Note:** The codebase imports `jose` (JWT encoding/decoding) and uses Pydantic `EmailStr` and FastAPI `OAuth2PasswordRequestForm`. Ensure `python-jose[cryptography]`, `email-validator`, and `python-multipart` are installed alongside `requirements.txt` if they are not already present in your environment.

---

## Installation

### Prerequisites

- **Python 3.10 or later**
- **pip** (Python package manager)
- **Docker** and **Docker Compose** (for the local PostgreSQL instance)
- **Git** (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone <repository-url>
cd taskflow
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install "python-jose[cryptography]" email-validator python-multipart
```

### 4. Configure environment variables

Copy the example environment file and edit it to match your local setup:

**Windows:**

```powershell
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Update `.env` with values aligned to your PostgreSQL credentials. When using the included Docker Compose service, use:

```env
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost:5432/taskflow
SECRET_KEY=<generate-a-strong-random-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | Async PostgreSQL connection string (`postgresql+asyncpg://...`) |
| `SECRET_KEY` | Secret used to sign JWT access tokens |
| `ALGORITHM` | JWT signing algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes |

> **Important:** The credentials in `docker-compose.yml` (`myuser` / `mypassword`) differ from the defaults in `.env.example` (`postgres` / `postgres`). Align your `.env` file with whichever database you run.

### 5. Start PostgreSQL

```bash
docker compose up -d postgres
```

Verify the container is running:

```bash
docker compose ps
```

### 6. Run database migrations

```bash
alembic upgrade head
```

This applies the initial migration (`3d88839e0e34`) creating the `users` and `tasks` tables.

---

## Usage

### Start the development server

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/` | Health/welcome endpoint |
| `http://127.0.0.1:8000/docs` | Swagger UI (interactive API documentation) |
| `http://127.0.0.1:8000/redoc` | ReDoc (alternative API documentation) |

### Example workflow

**1. Register a user**

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane",
    "email": "jane@example.com",
    "full_name": "Jane Doe",
    "password": "securepassword123"
  }'
```

Expected response (`201 Created`):

```json
{
  "id": 1,
  "username": "jane",
  "email": "jane@example.com",
  "full_name": "Jane Doe",
  "created_at": "2026-07-13T14:30:00Z"
}
```

**2. Obtain an access token**

```bash
curl -X POST http://127.0.0.1:8000/auth/Token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=jane&password=securepassword123"
```

Expected response (`200 OK`):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**3. Create a task**

```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write documentation",
    "description": "Update the project README",
    "status": "pending"
  }'
```

**4. List tasks (with optional filters)**

```bash
# All tasks (paginated)
curl http://127.0.0.1:8000/tasks/?skip=0&limit=10 \
  -H "Authorization: Bearer <access_token>"

# Filter by status
curl "http://127.0.0.1:8000/tasks/?status=pending" \
  -H "Authorization: Bearer <access_token>"
```

**5. Update a task**

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

**6. Delete a task**

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <access_token>"
```

Returns `204 No Content` on success.

### Server options

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

| Flag | Description |
|---|---|
| `--reload` | Auto-restart on code changes (development only) |
| `--host` | Bind address (default: `127.0.0.1`) |
| `--port` | Listen port (default: `8000`) |

---

## Project Structure

```
taskflow/
├── alembic/                        # Database migration tooling
│   ├── versions/
│   │   └── 3d88839e0e34_initial.py # Initial schema (users + tasks)
│   ├── env.py                      # Async Alembic environment config
│   ├── README                      # Alembic usage notes
│   └── script.py.mako              # Migration file template
├── app/
│   ├── core/
│   │   ├── config.py               # Pydantic settings (env vars)
│   │   ├── database.py             # Async engine, session factory, Base
│   │   └── security.py             # Password hashing, JWT creation
│   ├── crud/
│   │   ├── user.py                 # User create, authenticate, update
│   │   └── task.py                 # Task CRUD with owner scoping
│   ├── models/
│   │   ├── user.py                 # User SQLAlchemy model
│   │   └── task.py                 # Task SQLAlchemy model
│   ├── routers/
│   │   ├── auth.py                 # /auth routes (register, login, profile)
│   │   ├── task.py                 # /tasks routes (CRUD)
│   │   └── example.py              # Example scaffold (not mounted in main)
│   ├── schemas/
│   │   ├── enum.py                 # TaskStatus enum
│   │   ├── task.py                 # Task request/response schemas
│   │   └── user.py                 # User request/response schemas
│   ├── dependencies.py             # DB session + JWT auth dependencies
│   └── main.py                     # FastAPI app entrypoint
├── .env.example                    # Environment variable template
├── .gitignore
├── alembic.ini                     # Alembic configuration
├── docker-compose.yml              # PostgreSQL 17 service definition
├── requirements.txt                # Python dependencies
└── README.md
```

### Key modules

| Module | Responsibility |
|---|---|
| `app/main.py` | Instantiates the FastAPI app and mounts `auth` and `task` routers |
| `app/dependencies.py` | Provides `get_db()` session injection and `get_current_user()` JWT validation |
| `app/core/database.py` | Creates the async SQLAlchemy engine with SQL echo enabled for development |
| `app/models/` | Defines ORM entities; `User.tasks` cascades delete to owned tasks |
| `app/crud/` | Business logic separated from route handlers |
| `alembic/env.py` | Loads settings and model metadata for autogenerate migrations |

---

## API Documentation

All endpoints except `/`, `/auth/register`, and `/auth/Token` require a valid Bearer token in the `Authorization` header.

### Authentication

Authentication uses **OAuth2 Password Bearer** flow. After login, include the token on protected routes:

```
Authorization: Bearer <access_token>
```

The token URL configured for Swagger UI is `auth/Token`.

---

### Root

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/` | No | Returns a welcome message |

**Response:**

```json
{ "message": "Welcome to taskflow!" }
```

---

### Auth (`/auth`)

| Method | Path | Auth | Status | Description |
|---|---|---|---|---|
| `POST` | `/auth/register` | No | 201 | Register a new user |
| `POST` | `/auth/Token` | No | 200 | Login and receive JWT |
| `GET` | `/auth/me` | Yes | 200 | Get current user profile |
| `PUT` | `/auth/me` | Yes | 200 | Update current user profile |

#### `POST /auth/register`

**Request body:**

```json
{
  "username": "string",
  "email": "user@example.com",
  "full_name": "string | null",
  "password": "string"
}
```

**Response (`UserResponse`):**

```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "full_name": "string | null",
  "created_at": "2026-07-13T14:30:00Z"
}
```

**Errors:** `400` if username or email already exists.

#### `POST /auth/Token`

**Request:** `application/x-www-form-urlencoded`

| Field | Type | Description |
|---|---|---|
| `username` | string | Registered username |
| `password` | string | User password |

**Response (`TokenResponse`):**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Errors:** `401` for invalid credentials.

#### `PUT /auth/me`

**Request body (all fields optional):**

```json
{
  "username": "string | null",
  "email": "user@example.com | null",
  "full_name": "string | null",
  "password": "string | null"
}
```

---

### Tasks (`/tasks`)

All task endpoints require authentication. Tasks are scoped to the authenticated user; users cannot access other users' tasks.

| Method | Path | Status | Description |
|---|---|---|---|
| `GET` | `/tasks/` | 200 | List tasks (paginated, optional status filter) |
| `POST` | `/tasks/` | 201 | Create a task |
| `GET` | `/tasks/{task_id}` | 200 | Get a task by ID |
| `PATCH` | `/tasks/{task_id}` | 200 | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | 204 | Delete a task |

#### Query parameters — `GET /tasks/`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skip` | integer | `0` | Number of records to skip |
| `limit` | integer | `10` | Maximum records to return |
| `status` | string | — | Filter by status: `pending`, `in_progress`, `completed` |

#### `POST /tasks/` — Request body

```json
{
  "title": "string",
  "description": "string | null",
  "status": "pending"
}
```

#### `TaskResponse`

```json
{
  "id": 1,
  "title": "string",
  "description": "string | null",
  "status": "pending",
  "created_at": "2026-07-13T14:30:00Z",
  "updated_at": "2026-07-13T14:30:00Z"
}
```

#### `PATCH /tasks/{task_id}` — Request body (all fields optional)

```json
{
  "title": "string | null",
  "description": "string | null",
  "status": "pending | in_progress | completed | null"
}
```

**Errors:** `404` if the task does not exist or belongs to another user.

---

### Database schema

**`users`**

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | Primary key |
| `username` | String(50) | Unique, indexed |
| `email` | String(100) | Unique, indexed |
| `full_name` | String(100) | Nullable |
| `hashed_password` | String(255) | Not null |
| `created_at` | DateTime (TZ) | Server default: `now()` |

**`tasks`**

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String(100) | Not null |
| `description` | String(255) | Nullable |
| `status` | String(50) | Not null, default `pending` |
| `created_at` | DateTime (TZ) | Server default: `now()` |
| `updated_at` | DateTime (TZ) | Server default: `now()`, auto-updated |
| `owner_id` | Integer | Foreign key → `users.id` |

---

## Testing

This project does not currently include a test suite, test runner configuration, or CI pipeline. The `app/core/database.py` module includes a comment referencing test isolation patterns, but no `tests/` directory or pytest configuration exists.

To add testing in the future, a typical setup would include:

```bash
pip install pytest pytest-asyncio httpx
```

Suggested structure:

```
tests/
├── conftest.py          # Async test client and database fixtures
├── test_auth.py         # Registration, login, token validation
└── test_tasks.py        # Task CRUD and authorization
```

Run with:

```bash
pytest -v
```

Coverage (when configured):

```bash
pip install pytest-cov
pytest --cov=app --cov-report=term-missing
```

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. **Fork** the repository and create a feature branch from `main`.
2. **Follow existing conventions** — async route handlers, Pydantic schemas for I/O, CRUD logic in `app/crud/`, routes in `app/routers/`.
3. **Run migrations** — If you modify models, generate a new Alembic revision:
   ```bash
   alembic revision --autogenerate -m "describe your change"
   alembic upgrade head
   ```
4. **Keep secrets out of version control** — Never commit `.env` or credentials.
5. **Open a pull request** with a clear description of the change, motivation, and any migration or configuration steps required.
6. **Report issues** via the repository issue tracker, including Python version, steps to reproduce, and expected vs. actual behavior.

### Coding standards

- Use type hints on function signatures and return types.
- Prefer `async`/`await` for all database and route operations.
- Validate input with Pydantic models; return `response_model`-typed responses.
- Scope data access to the authenticated user where applicable.
- Use HTTP status codes consistently (`201` for creation, `204` for deletion, `404` for missing resources, `401` for auth failures).

---

## License

No license file is present in this repository. All rights to the source code are reserved by the project owner unless a license is added. Contact the repository maintainer for usage terms.

---

## Acknowledgments

- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern, high-performance web framework that powers the API layer and auto-generated documentation.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — Async ORM and database toolkit used for models, sessions, and queries.
- **[Alembic](https://alembic.sqlalchemy.org/)** — Database migration framework integrated with the async SQLAlchemy setup.
- **[pwdlib](https://github.com/frankie567/pwdlib)** — Password hashing library with Argon2 support.
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation and settings management.
- **[PostgreSQL](https://www.postgresql.org/)** — Relational database engine used for persistent storage.
- **[Uvicorn](https://www.uvicorn.org/)** — Lightning-fast ASGI server for running the application.
