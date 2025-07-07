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
        user_response = [self.dto.to_user_response(user) for user in users]
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

    def get_by_id(self, user_id, db):
        try:
            user: User = db.get(User, user_id)
            return self.dto.to_user_response(user)
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')

    def delete_by_id(self, user_id, db):
        try:
            user: User = db.get(User, user_id)
            db.delete(user)
        except Exception as e:
            logger.error(f'error deleting a user: {str(e)}')