from fastapi import APIRouter
from app.api.v1.endpoints import user

# Aggregate all v1 routers
api_router = APIRouter()
api_router.include_router(user.router)
