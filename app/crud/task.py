from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.task import Task
from app.models.user import User
from app.schemas.enum import TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

async def create_task(db: AsyncSession, task: TaskCreate, current_user: User) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        owner_id=current_user.id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_tasks(db: AsyncSession, current_user: User, skip: int, limit: int, status: TaskStatus | None = None) -> list[Task]:
    statement = select(Task).where(Task.owner_id == current_user.id)
    if status is not None:
        statement = statement.where(Task.status == status)
    statement = statement.offset(skip).limit(limit)
    result = await db.execute(statement)
    return list(result.scalars().all()) 

async def get_task_by_id(db: AsyncSession, task_id: int, current_user: User) -> Task | None:
    statement = select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()

async def update_task(db: AsyncSession, task: Task, task_update: TaskUpdate) -> Task:
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task    