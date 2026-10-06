from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.api.v1 import api_router as v1_router

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESC)

logger.info(
    "Service %s starting..!",
    settings.SERVICE_NAME
)

# Include the V1 API routes
app.include_router(v1_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint to verify service availability."""
    return {"status": "healthy"}
