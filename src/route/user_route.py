from fastapi import APIRouter, Request
from loguru import logger
from src.dao.schemas import CreateUserRequest
from src.service.user_service import UserService


class UserRoute:

    def __init__(self, user_service: UserService):
        self.router = APIRouter(prefix="/api/v1/users", tags=["Users"])
        self.user_service = user_service
        self.router.get("")(self.get_all)
        self.router.post("")(self.create_user)

    def get_all(self, request: Request):
        logger.info('fetching users')
        user_response = self.user_service.get_all(request.state.db)

        return user_response

    def create_user(self, user_data: CreateUserRequest, request: Request):
        self.user_service.create_user(user_data, request.state.db)