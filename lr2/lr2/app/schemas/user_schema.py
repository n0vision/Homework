from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    description: str | None = Field(default=None)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    description: str | None = None


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

