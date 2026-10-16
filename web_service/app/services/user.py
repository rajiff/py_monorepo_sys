from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import USER_EMAIL_UNIQUE_CONSTRAINT_NAME

class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        """
        Retrieve a user by their ID.
        """
        user = await self._repository.get_by_id(user_id)
        if not user or user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def get_user_by_email(self, email: str) -> UserRead:
        """
        Retrieve a user by their email address.
        """
        user = await self._repository.get_by_email(email)
        if not user or user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Create a new user record.
        """
        try:
            # Start the transaction before the first query. This avoids
            # conflicting with SQLAlchemy's implicit autobegin behavior.
            async with self._repository.transaction():
                existing_user = await self._repository.get_by_email(
                    user_data.email
                )

                if existing_user is not None:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email already registered",
                    )

                user = await self._repository.create(user_data)

            # Reached only after the transaction exits successfully.
            # The context manager has committed before this return.
            return user

        except IntegrityError as exc:
            # The database constraint is the final authority when
            # concurrent requests attempt to register the same email.
            if _is_email_unique_violation(exc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                ) from exc

            # Do not misreport unrelated integrity failures as duplicates.
            raise

    async def update_user(
        self,
        user_id: UUID,
        update_data: UserUpdate,
    ) -> UserRead:
        """
        Update an existing user record.
        """
        changes = update_data.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        try:
            async with self._repository.transaction():
                updated_user = await self._repository.update(
                    user_id,
                    update_data,
                )

                if updated_user is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found",
                    )

            return updated_user

        except IntegrityError as exc:
            if _is_email_unique_violation(exc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                ) from exc

            raise

def get_postgres_constraint_name(exc: IntegrityError) -> str | None:
    """Extract a constraint/index name from a database integrity error."""
    original = exc.orig

    # asyncpg and other drivers may expose the name differently.
    name = getattr(original, "constraint_name", None)

    # Some drivers expose PostgreSQL diagnostic details through .diag.
    if not name:
        diagnostic = getattr(original, "diag", None)
        name = getattr(diagnostic, "constraint_name", None)

    # Depending on the SQLAlchemy dialect, the underlying driver error
    # may be available through the original exception's cause.
    if not name:
        cause = getattr(original, "__cause__", None)
        name = getattr(cause, "constraint_name", None)

    return name

def _is_email_unique_violation(exc: IntegrityError) -> bool:
    return get_postgres_constraint_name(exc) == USER_EMAIL_UNIQUE_CONSTRAINT_NAME
