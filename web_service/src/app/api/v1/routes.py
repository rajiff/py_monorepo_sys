from fastapi import APIRouter
from app.api.v1 import user_profile

# Aggregate all v1 routers
api_router = APIRouter()
api_router.include_router(user_profile.router, prefix="/users", tags=["Users"])

