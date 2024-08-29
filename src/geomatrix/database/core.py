from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geomatrix.config import get_settings
from typing import AsyncGenerator, Annotated
from fastapi import Depends


settings = get_settings()

# async engine
async_engine = create_async_engine(
    url = settings.ASYNC_DB_URL,
    pool_size=settings.pool_size,
    echo=True,  # print SQL queries to console for debugging
    future=True
)

# async session
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
    )

# Base Class for orm
Base = declarative_base()

async def get_async_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session

async_db = Annotated[AsyncGenerator, Depends(get_async_db)]
