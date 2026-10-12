from typing import Optional
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by their unique identifier.
        """
        statement = select(User).where(User.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        """
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def create(self, user_data: UserCreate) -> User:
        """
        Create a new user record in the database.
        """
        db_user = User(**user_data.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, user_id: UUID, update_data: UserUpdate) -> Optional[User]:
        """
        Update an existing user record.
        """
        # Ensure we only update fields that are provided
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None

        statement = (
            update(User)
            .where(User.user_id == user_id)
            .values(**update_dict)
            .execution_options(synchronize_session=False)
        )

        await self.session.execute(statement)
        await self.session.commit()

        return await self.get_by_id(user_id)
