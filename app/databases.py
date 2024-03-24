from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


DB_URL: str = f"sqlite+aiosqlite:///./sql_app.db"


async_engine: AsyncEngine = create_async_engine(
    url=DB_URL,
    connect_args={
        "echo": True,
        "future": True,
        "check_same_thread": False,
    },
)

async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            print(e)


Session: AsyncSession = get_async_session()

