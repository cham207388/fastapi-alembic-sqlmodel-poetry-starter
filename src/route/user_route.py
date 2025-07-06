from fastapi import APIRouter, Request
from loguru import logger

from src.dao.db import user_session
from src.dao.schemas import CreateUserRequest
from src.service.user_service import UserService


class UserRoute:

    def __init__(self, user_service: UserService):
        self.router = APIRouter(prefix="/api/v1/users", tags=["Users"])
        self.user_service = user_service
        self.router.get("")(self.get_all)
        self.router.post("")(self.create_user)
        self.router.get("/{user_id}")(self.get_user_by_id)

    def get_all(self, user_sess: user_session, request: Request):
        self.user_service.auth_service.check_admin(user_sess)
        logger.info(f'{user_sess.get("email")} fetching users.')
        return self.user_service.get_all(request.state.db)


    def create_user(self, user_data: CreateUserRequest, request: Request):
        self.user_service.create_user(user_data, request.state.db)

    def get_user_by_id(self, user_id: int, user_sess: user_session, request: Request):
        self.user_service.auth_service.check_user(user_id, user_sess)
        logger.info(f'{user_sess.get("email")} retrieving info')
        return self.user_service.get_user_by_id(user_id, request.state.db)
