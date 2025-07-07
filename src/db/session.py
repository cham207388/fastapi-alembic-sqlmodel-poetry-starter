from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from typing import Annotated
from sqlmodel import create_engine

from src.core.constants import UN_AUTHENTICATED
from src.core.security import oauth2_bearer
from src.utils.env_vars import (
    secret_key, algorithm, db_user,db_password, db_host, db_port, db_name
)

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=False)

def get_db(request: Request) -> Session:
    return request.state.db
