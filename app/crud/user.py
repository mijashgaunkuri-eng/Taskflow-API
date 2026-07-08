from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate,LoginRequest
from app.core.security import get_password_hash, verify_password

#register a new user in the database
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    # Check if the user and email already exist
    statement = select(User).where(User.username == user.username)
    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    check_email_statement = select(User).where(User.email == user.email)
    email_result = await db.execute(check_email_statement)
    existing_email = email_result.scalar_one_or_none()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    #hash the password before storing it in the database
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

#authenticate a user by verifying their username and password
async def authenticate_user(db: AsyncSession, login_request: LoginRequest) -> User | None:
    statement = select(User).where(User.username == login_request.username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(login_request.password, user.hashed_password):
        return None
    return user