from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from typing import Annotated

from src.core.constants import UN_AUTHENTICATED
from src.core.env_vars import secret_key, algorithm

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db(request: Request) -> Session:
    return request.state.db

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
        email = payload.get('sub')
        user_id = payload.get('id')
        role = payload.get('role')
        if email is None or user_id is None:
            raise HTTPException(401, UN_AUTHENTICATED)
        return {"email": email, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(401, UN_AUTHENTICATED)

db_session = Annotated[Session, Depends(get_db)]
user_session = Annotated[dict, Depends(get_current_user)]