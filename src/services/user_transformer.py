from src.db.models import User, Role
from src.core.security import bcrypt_context
from src.schemas.user import CreateUserRequest, UpdateUserRequest, UserResponse

class UserTransformer:
    @staticmethod
    def to_user(request: CreateUserRequest) -> User:
        return User(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=bcrypt_context.hash(request.password),
            role=Role(request.role)
        )

    @staticmethod
    def to_user_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )

    @staticmethod
    def update_user(request: UpdateUserRequest, user: User):
        for field, value in request.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        return user 