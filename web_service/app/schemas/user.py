from typing import Optional
from uuid import UUID
from datetime import datetime, UTC
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.fields import Field
from sqlmodel import SQLModel

# Data Transfer Object

class UserBase(SQLModel):
    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="Unique email address")
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None

class UserRead(UserBase):
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
