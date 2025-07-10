from sqlmodel import select, Session
from loguru import logger

from src.schemas.user import CreateUserRequest
from src.services.auth_service import AuthService
from src.db.models import User
from src.utils.exceptions import BadRequestException, ServerException
from src.services.user_transformer import UserTransformer


class UserService:

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def get_all(self, db: Session):
        try:
            users = db.exec(select(User)).all()
            return [UserTransformer.to_user_response(user) for user in users]
        except Exception as e:
            raise ServerException(f'error creating user: {str(e)}')

    def create_user(self, user_data: CreateUserRequest, db: Session):
        logger.info(f'creating a user with email: {user_data.email}')
        user = UserTransformer.to_user(user_data)
        try:
            logger.info(f'user: {user}')
            db.add(user)
        except ValueError as e:
            logger.error(f'invalid value: {str(e)}')
            raise BadRequestException(f'invalid value: {str(e)}')
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
            raise ServerException(f'error creating user: {str(e)}')

    def get_by_id(self, user_id: int, db: Session):
        try:
            user: User = db.get(User, user_id)
            return UserTransformer.to_user_response(user)
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
            raise ServerException(f'error creating user: {str(e)}')

    def delete_by_id(self, user_id: int, db: Session):
        try:
            user: User = db.get(User, user_id)
            db.delete(user)
        except Exception as e:
            logger.error(f'error deleting a user: {str(e)}')
            raise ServerException(f'error creating user: {str(e)}')

    def update_user(self, user_id, user_data, db_session: Session):
        try:
            saved_user: User = db_session.get(User, user_id)
            user = UserTransformer.update_user(user_data, saved_user)
            db_session.commit()
            db_session.refresh(user)
            return UserTransformer.to_user_response(user)
        except ValueError as e:
            logger.error(f'invalid value: {str(e)}')
            raise BadRequestException(f'invalid value: {str(e)}')
        except Exception as e:
            logger.error(f'error creating user: {str(e)}')
            raise ServerException(f'error updating user: {str(e)}')