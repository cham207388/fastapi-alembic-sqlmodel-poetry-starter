from sqlmodel import select
from loguru import logger

from src.schemas.user import Dto
from src.services.auth_service import AuthService
from src.db.models import User


class UserService:

    def __init__(self, auth_service: AuthService, dto: Dto):
        self.auth_service = auth_service
        self.dto = dto

    def get_all(self, db):
        users = db.exec(select(User)).all()
        user_response = [self.dto.convert_to_user_response(user) for user in users]
        return user_response

    def create_user(self, user_req: User, db):
        logger.info(f'creating a user with email: {user_req.email}')
        logger.info(f'user_req: {user_req}')
        try:
            user: User = self.dto.to_user(user_req)
            logger.info(f'user: {user}')
            db.add(user)
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
