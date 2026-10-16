from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Optional
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.logger import logger

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.logger = logger

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        """
        Provide a transaction boundary for the calling use case.

        Successful exit commits. An exception escaping the block rolls back.
        Start this boundary before executing queries that could autobegin
        a transaction on the session.
        """
        async with self.__session.begin():
            yield

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by their unique identifier.
        """
        statement = select(User).where(User.user_id == user_id)
        result = await self.__session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        """
        statement = select(User).where(User.email == email)
        result = await self.__session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        """
        Create a new user record in the database.
        Stage a new user and flush it without committing.
        """
        db_user = User(**user_data.model_dump())

        self.__session.add(db_user)

        # allows database-generated values and constraint violations to
        # become visible before the service finishes the use case.
        # The transaction is still open.
        await self.__session.flush()

        # Flush sends SQL and surfaces many database errors here.
        # It does not commit; the surrounding transaction owns that.
        return db_user

    async def update(
        self,
        user_id: UUID,
        update_data: UserUpdate,
    ) -> User | None:
        """
        Update a user and return the updated row, without committing.
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        if not update_dict:
            return None

        statement = (
            update(User)
            .where(User.user_id == user_id)
            .values(**update_dict)
            .returning(User) # avoids an additional query to retrieve
            .execution_options(synchronize_session=False)
        )

        try:
            result = await self.__session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as exc:
            self.logger.error(
                "Database error during update for user %s: %s",
                user_id,
                exc,
                exc_info=True)
            raise
