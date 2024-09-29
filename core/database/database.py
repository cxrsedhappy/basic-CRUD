from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from core.config import setting


Base = declarative_base()

engine = create_async_engine(
    url=setting.DB_URL,
    echo=setting.DB_ECHO
)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def global_init():
    """Database initialization. Drops existing tables and creates new"""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def create_session() -> AsyncSession:
    async with session_factory() as session:
        yield session
