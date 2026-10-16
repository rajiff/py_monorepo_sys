from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import USER_EMAIL_UNIQUE_CONSTRAINT_NAME
from app.core.logger import logger

class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository
        self.logger = logger

    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        """
        Retrieve a user by their ID.
        """
        self.logger.debug("Fetching user with ID: %s", user_id)
        user = await self._repository.get_by_id(user_id)
        if not user or user is None:
            self.logger.warning("User lookup failed: %s not found", user_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def get_user_by_email(self, email: str) -> UserRead:
        """
        Retrieve a user by their email address.
        """
        self.logger.debug("Fetching user with email: %s", email)
        user = await self._repository.get_by_email(email)
        if not user or user is None:
            self.logger.warning("User lookup failed for email: %s not found", email)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Create a new user record.
        """
        self.logger.info("Attempting to create user with email: %s", user_data.email)
        try:
            # Start the transaction before the first query. This avoids
            # conflicting with SQLAlchemy's implicit autobegin behavior.
            async with self._repository.transaction():
                existing_user = await self._repository.get_by_email(
                    user_data.email
                )

                if existing_user is not None:
                    self.logger.warning("Registration failed: Email already registered: %s", user_data.email)
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email already registered",
                    )

                user = await self._repository.create(user_data)

            # Reached only after the transaction exits successfully.
            # The context manager has committed before this return.
            self.logger.info("User successfully created with ID: %s", user.user_id)
            return user

        except IntegrityError as exc:
            if _is_email_unique_violation(exc):
                self.logger.warning("Database-level registration failed: Email already registered: %s", user_data.email)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                ) from exc

            self.logger.error("Database integrity error during user creation: %s", exc, exc_info=True)
            raise

    async def update_user(
        self,
        user_id: UUID,
        update_data: UserUpdate
    ) -> UserRead:
        """
        Update an existing user record.
        """
        self.logger.debug("Initiating update for user: %s", user_id)
        changes = update_data.model_dump(exclude_unset=True)

        if not changes:
            self.logger.warning("Update ignored for user %s: No changes provided", user_id)
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
                    self.logger.warning("Update failed: User %s not found", user_id)
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found",
                    )

            self.logger.info("User %s updated successfully", user_id)
            return updated_user

        except IntegrityError as exc:
            if _is_email_unique_violation(exc):
                self.logger.warning("Update failed: Email conflict for user %s", user_id)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                ) from exc

            self.logger.error(
                "Database integrity error during user update: %s",
                exc, exc_info=True)
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

