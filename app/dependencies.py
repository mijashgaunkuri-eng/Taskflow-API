from app.core.database import AsyncSessionLocal #core/database.py bata SessionLocal import gareko ho, jasko kaam database session create garne ho
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession #sQLAlchemy ko AsyncSession import gareko ho, jasko kaam asynchronous database session handle garne ho
from typing import AsyncGenerator
from sqlalchemy import select
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/Token")

async def get_db() -> AsyncGenerator[AsyncSession, None]:#database session generator function that yields an asynchronous database session for use in FastAPI endpoints
    async with AsyncSessionLocal() as session:
        yield session 

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(payload)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
