from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.db_config import DatabaseConfig

def create_database_engine(settings: DatabaseConfig):
    """
    Construct the SQLAlchemy async engine and connection pool.
    The engine is the application's long-lived database connectivity resource

    This function configures the engine but does not own its lifecycle.
    The application lifespan is responsible for disposing it at shutdown.

    The engine manages database connectivity and reuses physical connections.
    It does not open a connection immediately just because the engine was created.

    will be called usually during the application startup.

    """

    db_engine: AsyncEngine = create_async_engine(
        settings.DB_URL,

        # Enable SQL statement logging only when explicitly configured.
        # SQL logs may expose sensitive values and can be noisy in production.
        # Never enable verbose SQL logging unconditionally in production.
        echo=settings.DB_ECHO_SQL_LOGGING,

        # Bound the number of pooled connections and how long a caller
        # waits to obtain one. Capacity must be considered across all
        # application worker processes and replicas.
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,

        # Recycle old connections and validate connections on checkout.
        # Recycle older pooled connections and validate a connection
        # before checkout to reduce failures from stale connections.
        pool_recycle=settings.DB_POOL_RECYCLE,
        pool_pre_ping=settings.DB_POOL_PRE_PING,

        # Driver-specific: appropriate for asyncpg.
        # asyncpg driver connection-establishment timeout, in seconds.
        # This is distinct from pool_timeout, which limits pool checkout.
        connect_args={
            "timeout": settings.DB_CONNECT_TIMEOUT,
        },
    )

    return db_engine

@asynccontextmanager
async def db_engine_lifespan(app: FastAPI, settings: DatabaseConfig):
    """
    Own the database resources for the application's lifespan.

    Startup:
      1. Load database configuration.
      2. Create the engine and session factory.
      3. Verify that the database can be reached.
      4. Publish the resources through app.state.

    Shutdown:
      Dispose of the engine and release its pooled connections.

    Detects database unavailability during startup.
        Creates the engine and session factory during application startup,
        verifies database connectivity with SELECT 1,
        makes the resources available through app.state, and
        disposes the engine when the application shuts down.

    This is an async context manager intended to be entered by the
    application's main lifespan function.

    """

    # Create one engine per application process, not one per request.
    engine = create_database_engine(settings)

    # The factory creates independent AsyncSession instances that share
    # the engine. expire_on_commit=False keeps loaded ORM attributes
    # accessible after commit without automatic expiration and reload.
    db_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False, # ORM attributes are not automatically expired after commit
        # autoflush=False,
    )

    try:
        # Fail startup if the database cannot be reached at this point.
        # This is a connectivity check, not a guarantee that the database
        # PS: The database could fail a moment later
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        # Share the engine and factory with FastAPI dependencies.
        # Store the factory, not a single session: each request needs
        # its own session rather than sharing mutable session state.
        app.state.db_engine = engine
        app.state.db_session_factory = db_session_factory

        # Yield control to FastAPI while the application is running.
        yield

    finally:
        # Dispose pooled connections on normal shutdown or startup failure.
        # Sessions should already have completed their request-scoped work.
        await engine.dispose()

async def get_session(
    request: Request,
) -> AsyncIterator[AsyncSession]:
    """
    Generator function that provides a session for each request.

    FastAPI dependency that provides a request-scoped AsyncSession.

    Gives each dependency invocation its own session
        Retrieves the application-wide session factory, creates an independent
        session, yields it to the dependent endpoint/service/repository, and
        closes it when dependency execution finishes.

    Closing the session releases its connection resources and rolls back
    any still-active uncommitted transaction. It does not automatically
    commit successful writes.

    Transaction boundaries and commit/rollback policy belong to the
    application use case or service layer, not this generic dependency.

    It closes that session when the dependency finishes, including
    when request processing raises an exception.

    """

    # The AsyncSession represents a unit of ORM interaction and transaction state.
    session_factory = cast(
        async_sessionmaker[AsyncSession],
        request.app.state.db_session_factory,
    )

    # The context manager guarantees session cleanup, including on exceptions.
    async with session_factory() as session:
        yield session
