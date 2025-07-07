from http import HTTPStatus
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
        self.router.post("", status_code=HTTPStatus.CREATED)(self.create_user)
        self.router.get("/{user_id}")(self.get_by_id)
        self.router.delete("/{user_id}")(self.delete_by_id)

    def get_all(self, request: Request) -> List[UserResponse]:
        logger.info('fetching users')
        return self.user_service.get_all(request.state.db)

    def create_user(self, user_data: CreateUserRequest, request: Request):
        logger.info('creating a user.')
        self.user_service.create_user(user_data, request.state.db)

    def get_by_id(self, user_id, request: Request):
        logger.info('getting a user by id.')
        return self.user_service.get_by_id(user_id, request.state.db)

    def delete_by_id(self, user_id, request: Request):
        logger.info('getting a user by id.')
        return self.user_service.delete_by_id(user_id, request.state.db)
