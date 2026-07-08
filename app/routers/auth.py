from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import TokenResponse, UserCreate, UserResponse, LoginRequest
from app.crud.user import create_user, authenticate_user
from app.dependencies import get_db
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    
    return await create_user(db, user)

@router.post("/Token", response_model=TokenResponse)
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, login_request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub":user.username} , expires_delta=30)  # Token expires in 30 minutes
    return {"access_token": access_token, "token_type": "bearer"}
    


