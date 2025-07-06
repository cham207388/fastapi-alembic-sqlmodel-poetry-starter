from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from typing import Annotated

from src.util.constants import oauth2_bearer, UN_AUTHENTICATED
from src.util.env_vars import secret_key, algorithm, DATABASE_URL
from sqlmodel import create_engine

engine = create_engine(DATABASE_URL, echo=False)


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
