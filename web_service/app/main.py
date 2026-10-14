from contextlib import AsyncExitStack, asynccontextmanager
from fastapi import FastAPI

from app.api.v1.routes import api_router as api_v1_router

from app.core.config import config
from app.core.db_config import DatabaseConfig

from app.core.logger import logger_lifespan
from app.core.database import db_engine_lifespan

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Lifecycle management for the FastAPI application."""

    db_settings = DatabaseConfig()

    async with AsyncExitStack() as stack:
        await stack.enter_async_context(logger_lifespan(app)) # logger first
        await stack.enter_async_context(db_engine_lifespan(app, db_settings))

        yield

app = FastAPI(
        title=config.SERVICE_NAME,
        description=config.SERVICE_DESC,
        lifespan=app_lifespan
    )

# Include the V1 API routes
app.include_router(api_v1_router, prefix="/api/v1")
