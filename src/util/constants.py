from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

UN_AUTHENTICATED = "Incorrect email/password combination!"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
