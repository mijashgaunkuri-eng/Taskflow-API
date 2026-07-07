from dotenv import load_dotenv
import os

from app.core.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

load_dotenv()


def get_database_url() -> str:
    return os.getenv('DATABASE_URL', 'sqlite:///./taskflow.db')


#get database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
