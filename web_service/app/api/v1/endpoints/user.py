from uuid import UUID
from datetime import datetime, UTC
from fastapi import APIRouter, status
from app.dependencies.user import UserServiceDep
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=UserRead)
async def current_user(
    service: UserServiceDep
) -> UserRead:
    """
    Retrieve the current user's information.
    """
    # For now, just a placeholder, we don't have a list method in service
    # but it's good to have the structure
    user_info = UserRead(
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
    return user_info

@router.get("/{user_email}", response_model=UserRead)
async def get_user_by_email(
    user_email: str,
    service: UserServiceDep
) -> UserRead:
    """
    Get a user by their email address.
    """
    # return await service.get_user_by_id(user_id)
    return await service.get_user_by_email(user_email)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: UserServiceDep
) -> UserRead:
    """
    Create a new user.
    """
    return await service.create_user(user_data)

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    update_data: UserUpdate,
    service: UserServiceDep
) -> UserRead:
    """
    Update an existing user's information.
    """
    return await service.update_user(user_id, update_data)
