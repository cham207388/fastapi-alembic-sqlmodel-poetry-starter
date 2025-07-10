from datetime import datetime, timezone
from typing import Optional

from pydantic import EmailStr, field_validator, ConfigDict
from sqlmodel import Field, SQLModel

from src.core.security import bcrypt_context
from src.db.models import Role, User


class CreateUserRequest(SQLModel):
    email: EmailStr  # ✅ Enforces email validation
    first_name: str = Field(..., min_length=3, max_length=15)
    last_name: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=3, max_length=15)
    role: str


    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "username@email.com",
                "first_name": "First Name",
                "last_name": "Last Name",
                "password": "password",
                "role": "user",
            }
        }
    )

    @field_validator("first_name", "last_name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

class UpdateUserRequest(SQLModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(default=None, min_length=3, max_length=15)
    last_name: Optional[str] = Field(default=None, min_length=3, max_length=15)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "updated@email.com",
                "first_name": "Updated First",
                "last_name": "Updated Last",
            }
        }
    )

    @field_validator("first_name", "last_name")
    def validate_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Name cannot be empty")
        return value

class UserResponse(SQLModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: Role
