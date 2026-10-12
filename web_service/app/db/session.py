from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.db_config import DatabaseConfig

# Initialize database configuration
db_settings = DatabaseConfig()
DATABASE_URL = db_settings.DB_URL

# Create the asynchronous engine
# We use echo=True for development to see the SQL queries
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=db_settings.DB_POOL_SIZE,
    max_overflow=db_settings.DB_MAX_OVERFLOW,
    pool_recycle=db_settings.DB_POOL_RECYCLE,
    pool_pre_ping=db_settings.DB_POOL_PRE_PING,
    connect_args={"timeout": db_settings.DB_POOL_TIMEOUT}
)

# Create a session factory
# Note: expire_on_commit=False is required for AsyncSession
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an async database session for each request.
    """
    async with async_session_maker() as session:
        yield session
