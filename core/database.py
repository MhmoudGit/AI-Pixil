from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Generator
from fastapi.responses import ORJSONResponse
from .settings import settings


# 'postgresql://<username>:<password>@<ip-adress/hostname>:portnumber/<database_name>'
DATABASE_URL: str = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"


engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)


async def get_session() -> Generator[AsyncSession, Any, None]:
    async with async_session() as session:
        assert isinstance(session, AsyncSession)
        yield session


Base: DeclarativeMeta = declarative_base()


async def connect() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Database is connected successfully...")


async def disconnect() -> None:
    if engine:
        await engine.dispose()
        print("database is disconnected successfully...")


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator:
    try:
        await connect()
        yield
    finally:
        await disconnect()


app_configs: dict[str, Any] = {
    "lifespan": lifespan,
    "title": "AI Pixil",
    "debug": True,
    "default_response_class": ORJSONResponse,
    "description": "API for generating Pixel art stickers using AI",
}
