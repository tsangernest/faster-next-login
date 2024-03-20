from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)


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
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

