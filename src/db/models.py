from enum import Enum
from pydantic import EmailStr, field_validator
from typing import Optional
from sqlmodel import Field, SQLModel


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    hashed_password: str = Field(max_length=200, nullable=False, exclude=True)
    role: Role = Field(default=Role.USER, nullable=False)

    @field_validator("first_name", "last_name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value
