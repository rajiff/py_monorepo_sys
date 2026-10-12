from typing import Optional
from datetime import datetime, UTC
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import DateTime, text

class User(SQLModel, table=True):
    __tablename__ = "users"
    # __primary_key=True

    # Note: We use PG_UUID for the type hint but default to UUID for compatibility
    user_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )

    # Multi-tenancy Field
    # tenant_id: UUID = Field(sa_type=PG_UUID, nullable=False, indexing=True)

    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None

    # Metadata fields
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),  # ✅ Generates fresh time on creation
        sa_type=DateTime(timezone=True),  # ✅ Correctly sets TIMESTAMPTZ type
        sa_column_kwargs={"server_default": text("NOW()")}  # ✅ Safe place for raw SQL text
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),  # ✅ Generates fresh time on creation
        sa_type=DateTime(timezone=True),  # ✅ Correctly sets TIMESTAMPTZ type
        sa_column_kwargs={
            "server_default": text("NOW()"),
            "onupdate": text("NOW()")  # ✅ Automatically updates on row modification
        }
    )
