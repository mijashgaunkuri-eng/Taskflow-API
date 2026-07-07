from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

#engine 
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True) 

#session maker
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

#Base class for models
Base = declarative_base()

# each session has its own transaction, which is rolled back at the end of the request, so that the database is not affected by tests.        