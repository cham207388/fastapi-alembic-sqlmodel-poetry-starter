from sqlmodel import select, Session
from loguru import logger

from src.schemas.user import Dto, CreateUserRequest
from src.services.auth_service import AuthService
from src.db.models import User
from src.utils.exceptions import BadRequestException, ServerException


class UserService:

    def __init__(self, auth_service: AuthService, dto: Dto):
        self.auth_service = auth_service
        self.dto = dto

    def get_all(self, db):
        try:
            users = db.exec(select(User)).all()
            return [self.dto.to_user_response(user) for user in users]
        except Exception as e:
            raise ServerException(f'error creating user: {str(e)}')

    def create_user(self, user_data: CreateUserRequest, db):
        logger.info(f'creating a user with email: {user_data.email}')
        user = self.dto.to_user(user_data)
        try:
            logger.info(f'user: {user}')
            db.add(user)
        except ValueError as e:
            logger.error(f'invalid value: {str(e)}')
            raise BadRequestException(f'invalid value: {str(e)}')
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
            raise ServerException(f'error creating user: {str(e)}')

    def get_by_id(self, user_id, db):
        try:
            user: User = db.get(User, user_id)
            return self.dto.to_user_response(user)
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
            raise ServerException(f'error creating user: {str(e)}')

    def delete_by_id(self, user_id, db):
        try:
            user: User = db.get(User, user_id)
            db.delete(user)
        except Exception as e:
            logger.error(f'error deleting a user: {str(e)}')
            raise ServerException(f'error creating user: {str(e)}')

    def update_user(self, user_id, user_data, db_session: Session):
        try:
            saved_user: User = db_session.get(User, user_id)
            user = self.dto.update_user(user_data, saved_user)
            db_session.commit()
            db_session.refresh(user)
            return self.dto.to_user_response(user)
        except ValueError as e:
            logger.error(f'invalid value: {str(e)}')
            raise BadRequestException(f'invalid value: {str(e)}')
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
            raise ServerException(f'error updating user: {str(e)}')