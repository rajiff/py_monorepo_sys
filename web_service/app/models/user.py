from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, String, func, text
from sqlmodel import Field, SQLModel

USER_EMAIL_UNIQUE_CONSTRAINT_NAME = "uq_users_email_ci"
USER_USERNAME_UNIQUE_CONSTRAINT_NAME = "uq_users_username_ci"

class User(SQLModel, table=True):
    __tablename__ = "users"

    # PostgreSQL creates an index for the primary key automatically.
    user_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("uuidv4()"),
        },
    )

    # Uniqueness is enforced case-insensitively by the indexes below.
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)

    name: str | None = Field(default=None)
    phone: str | None = Field(default=None, sa_type=String(20))
    city: str | None = Field(default=None, sa_type=String(255))
    pincode: str | None = Field(default=None, sa_type=String(10))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("NOW()")},
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": text("NOW()"),
            "onupdate": text("NOW()"),
        },
    )


# PostgreSQL expression indexes enforce case-insensitive uniqueness.
Index(
    USER_USERNAME_UNIQUE_CONSTRAINT_NAME,
    func.lower(User.username),
    unique=True,
)

Index(
    USER_EMAIL_UNIQUE_CONSTRAINT_NAME,
    func.lower(User.email),
    unique=True,
)
