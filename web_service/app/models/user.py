from typing import Optional
from datetime import datetime, UTC
from uuid import UUID
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import text

class User(SQLModel, table=True):
    __tablename__ = "users"
    __primary_key=True

    # Note: We use PG_UUID for the type hint but default to UUID for compatibility
    user_id: UUID = Field(
        default=None,
        primary_key=True,
        sa_type=PG_UUID,
        indexing=True
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
        default_factory=datetime.now(UTC),
        sa_type=text("TIMESTAMPTZ DEFAULT NOW()")
    )
    updated_at: datetime = Field(
        default_factory=datetime.now(UTC),
        sa_type=text("TIMESTAMPTZ DEFAULT NOW()")
    )
