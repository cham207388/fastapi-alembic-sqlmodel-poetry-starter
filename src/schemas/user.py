from datetime import datetime, timezone

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

class UserResponse(SQLModel):
    id: int
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
            role=Role(request.role)
        )

    def to_user_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )
# ,
#             created_at=datetime.now(timezone.utc),
#             updated_at=datetime.now(timezone.utc),
#             created_by=request.email,
#             updated_by=request.email