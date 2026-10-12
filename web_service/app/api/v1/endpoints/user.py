from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency Injection
async def get_user_repository() -> UserRepository:
    async with get_session() as session:
        yield UserRepository(session)

async def get_user_service() -> UserService:
    async for repo in get_user_repository():
        return UserService(repo)

@router.get("/", response_model=UserRead)
async def current_user(
    service: UserService = Depends(get_user_service)
) -> UserRead:
    # For now, just a placeholder, we don't have a list method in service
    # but it's good to have the structure
    current_user = UserRead(
        username = "current_user",
        email = "current_user@example.com",
        name= "Current User",
        phone= "1234567890",
        city= "New York",
        pincode= "10001",
        user_id = "f0589879-eff6-41b4-8267-52cfbcab4aab",
        created_at = datetime.now(UTC),
        updated_at = datetime.now(UTC)
    )
    return current_user

@router.get("/{user_email}", response_model=UserRead)
async def get_user_by_email(
    user_email: str,
    service: UserService = Depends(get_user_service)
) -> UserRead:
    # return await service.get_user_by_id(user_id)
    return await service.get_user_by_email(user_email)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
) -> UserRead:
    return await service.create_user(user_data)

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    update_data: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> UserRead:
    return await service.update_user(user_id, update_data)
