from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user
from app.dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    
    return await create_user(db, user)

