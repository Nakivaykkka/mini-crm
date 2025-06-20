from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

class Base(DeclarativeBase):
    pass

settings = get_settings()


if settings.SQLALCHEMY_DATABASE_URL.startswith("postgresql+asyncpg"):
    async_engine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URL,
        echo=False
    )
    
    async_sessionmaker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
    
    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_sessionmaker() as session:
            yield session
        
else:
    async_engine = None
    async_sessionmaker = None
    
    async def get_async_session() -> None:
        raise RuntimeError("get_async_session не работает в sync режиме (alembic)")
        
        