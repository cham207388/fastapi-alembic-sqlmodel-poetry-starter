from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from jose import jwt
from loguru import logger
from sqlmodel import select

from src.dao.models import Role, User
from src.util.env_vars import secret_key, algorithm
from src.util.constants import UN_AUTHENTICATED, bcrypt_context


class AuthService:

    def authenticate_user(self, email: str, password: str, db):
        stmt = select(User).where(User.email == email)
        user: User = db.exec(stmt).first()
        logger.debug(f'authenticating user {user.email}')
        if user and self.verify_password(password, user.hashed_password):
            access_token = self.create_access_token(
                email, user.id, user.role, timedelta(minutes=20))
            return {'access_token': access_token, 'token_type': 'bearer'}
        raise HTTPException(401, UN_AUTHENTICATED)

    def verify_password(self, password, hashed_password):
        return bcrypt_context.verify(password, hashed_password)

    def bcrypt_hash_password(self, password):
        return bcrypt_context.hash(password)

    def create_access_token(self, email: str, user_id: int, role: str, expires_delta: timedelta):
        logger.debug(f"Creating access token for: {email}")
        expires = datetime.now(timezone.utc) + expires_delta
        encode = {"sub": email, "id": user_id, "role": role, "exp": expires}
        return jwt.encode(encode, secret_key, algorithm=algorithm)

    def check_user(self, user_id, user_sess):
        logger.debug(f"User {user_sess}")
        if user_sess is None or user_sess.get("id") != user_id:
            logger.warning("Authentication Failed!")
            raise HTTPException(401, "Authentication Failed!")

    def check_admin(self, user_sess):
        if user_sess is None or user_sess.get('role') != Role.ADMIN:
            raise HTTPException(403, "Authorization Failed!")