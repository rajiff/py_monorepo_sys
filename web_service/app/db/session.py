from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.db_config import DatabaseConfig

# Initialize database configuration
db_settings = DatabaseConfig()

# Create the asynchronous engine
# We use echo=True for development to see the SQL queries
engine = create_async_engine(
    db_settings.DB_URL,
    echo=db_settings.DB_ECHO_SQL_LOGGING,

    pool_size=db_settings.DB_POOL_SIZE,
    max_overflow=db_settings.DB_MAX_OVERFLOW,
    pool_timeout=db_settings.DB_POOL_TIMEOUT,

    pool_recycle=db_settings.DB_POOL_RECYCLE,
    pool_pre_ping=db_settings.DB_POOL_PRE_PING,

    connect_args={"timeout": db_settings.DB_CONNECT_TIMEOUT}
)

# Create a session factory
# Note: expire_on_commit=False is required for AsyncSession
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # ORM attributes are not automatically expired after commit
    autoflush=False, # prevents automatic flushes before queries
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an async database session for each request.
    """
    async with async_session_maker() as session:
        yield session
