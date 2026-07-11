
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserResponse, LoginRequest, UpdateUser
from app.crud.user import create_user, authenticate_user, update_user
from app.dependencies import get_db, get_current_user
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    
    return await create_user(db, user)

@router.post("/Token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, LoginRequest(username=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub":user.username} , expires_delta=30)  # Token expires in 30 minutes
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_info(update_data: UpdateUser, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db, current_user, update_data)
    return updated_user
