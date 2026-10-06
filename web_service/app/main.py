from fastapi import FastAPI

from app.api.v1.routes import api_router as api_v1_router

from app.core.config import config
from app.core.logger import logger

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
