from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.services.auth_service import AuthService


class AuthRoute:

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
        self.router.post("/login")(self.login)

    def login(self, login_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
        return self.auth_service.authenticate_user(login_data.username, login_data.password, request.state.db)