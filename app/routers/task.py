from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import create_task, get_tasks, update_task, delete_task
from app.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.get("/" , response_model=list[TaskResponse])
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = await get_tasks(db, current_user, skip=skip, limit=limit)
    return tasks