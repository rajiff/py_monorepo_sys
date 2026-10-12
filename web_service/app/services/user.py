from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        """
        Retrieve a user by their ID.
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def get_user_by_email(self, email: str) -> UserRead:
        """
        Retrieve a user by their email address.
        """
        user = await self.repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Create a new user record.
        """
        # Business logic: Check if email is already registered
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = await self.repository.create(user_data)
        return user

    async def update_user(self, user_id: UUID, update_data: UserUpdate) -> UserRead:
        """
        Update an existing user record.
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        updated_user = await self.repository.update(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update failed"
            )
        return updated_user
