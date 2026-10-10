from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.routes import api_router as api_v1_router

from app.core.config import config
from app.core.logger import logger

@asynccontextmanager
async def lifespan(_):
    """Lifecycle management for the FastAPI application."""
    # STARTUP
    logger.info("*** Starting service: %s", config.SERVICE_NAME)
    yield
    # SHUTDOWN
    logger.info("*** Shutting down service: %s", config.SERVICE_NAME)

app = FastAPI(title=config.SERVICE_NAME,
              description=config.SERVICE_DESC)

logger.info(
    "Service %s starting..!",
    config.SERVICE_NAME
)

# Include the V1 API routes
app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint to verify service availability."""
    return {"status": "ok"}
