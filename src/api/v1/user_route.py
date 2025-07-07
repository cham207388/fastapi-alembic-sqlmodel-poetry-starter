from typing import List

from fastapi import APIRouter, Request
from loguru import logger
from src.schemas.user import CreateUserRequest, UserResponse
from src.services.user_service import UserService


class UserRoute:

    def __init__(self, user_service: UserService):
        self.router = APIRouter(prefix="/api/v1/users", tags=["Users"])
        self.user_service = user_service
        self.router.get("", response_model=List[UserResponse])(self.get_all)
        self.router.post("")(self.create_user)

    def get_all(self, request: Request) -> List[UserResponse]:
        logger.info('fetching users')
        return self.user_service.get_all(request.state.db)

    def create_user(self, user_data: CreateUserRequest, request: Request):
        self.user_service.create_user(user_data, request.state.db)