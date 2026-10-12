from fastapi import APIRouter
from app.api.v1.endpoints import user
from app.api.v1.endpoints.health import router as health_router

# Aggregate all v1 routers
api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(health_router)
