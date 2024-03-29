from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel


DB_URL: str = f"sqlite+aiosqlite:///./sql_app.db"


async_engine: AsyncEngine = create_async_engine(
    url=DB_URL,
    echo=True,
    future=True,
)


async def initialize_database():
    async with async_engine.begin() as eng_conn:
        await eng_conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autocommit=False,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

