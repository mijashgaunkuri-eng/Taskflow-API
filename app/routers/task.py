from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.enum import TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import create_task, get_task_by_id, get_tasks, update_task, delete_task
from app.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.get("/" , response_model=list[TaskResponse])
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user), status: TaskStatus | None = None):
    tasks = await get_tasks(db, current_user, skip=skip, limit=limit, status=status)
    return tasks\
    
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    new_task = await create_task(db, task, current_user)
    return new_task

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated_task = await update_task(db, task, task_update)
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await delete_task(db, task)
    return None
        