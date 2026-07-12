from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.task import Task
from app.models.user import User
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

async def get_tasks(db: AsyncSession, current_user: User, skip: int, limit: int) -> list[Task]:
    statement = select(Task).where(Task.owner_id == current_user.id)
    statement = statement.offset(skip).limit(limit)
    result = await db.execute(statement)
    return list(result.scalars().all()) 

async def update_task(db: AsyncSession, task: Task, update_data: TaskUpdate) -> Task:
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None:
            setattr(task, key, value)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()