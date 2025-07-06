from typing import Optional

from pydantic import EmailStr, field_validator, ConfigDict
from sqlmodel import Field, SQLModel

from src.dao.models import User, Role
from src.util.constants import bcrypt_context


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

class UserResponse(SQLModel):
    email: str
    first_name: str
    last_name: str
    role: Role

class Dto:
    def to_user(self, request: CreateUserRequest) -> User:
        return User(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=bcrypt_context.hash(request.password),
            # role=Role.USER if request.role == 'user' else Role.ADMIN
            role=Role(request.role)
        )

    def to_user_response(self, user: User) -> UserResponse:
        return UserResponse(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )