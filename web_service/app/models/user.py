from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, String, func, text
from sqlmodel import Field, SQLModel

IDX_USERS_UNIQUE_EMAIL = "idx_uq_users_email_ci"
IDX_USERS_UNIQUE_USERNAME = "idx_uq_users_username_ci"

IDX_USERS_NAME = "idx_users_name_ci"
IDX_USERS_CITY = "idx_users_city_ci"
IDX_USERS_PINCODE = "idx_users_pincode_ci"

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
    pincode: str | None = Field(default=None, sa_type=String(20))
    country: str | None = Field(default=None, sa_type=String(255))

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
    IDX_USERS_UNIQUE_USERNAME,
    func.lower(User.username),
    unique=True,
)

Index(
    IDX_USERS_UNIQUE_EMAIL,
    func.lower(User.email),
    unique=True,
)

Index(
    IDX_USERS_NAME,
    func.lower(User.name),
    unique=False
)

Index(
    IDX_USERS_CITY,
    func.lower(User.city),
    unique=False
)

Index(
    IDX_USERS_PINCODE,
    func.lower(User.pincode),
    unique=False
)
