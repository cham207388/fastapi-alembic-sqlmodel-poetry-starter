from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from jose import JWTError, jwt

from src.util.env_vars import secret_key, algorithm

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                scheme, token = auth_header.split()
                if scheme.lower() != "bearer":
                    raise ValueError("Invalid scheme")

                payload = decode_jwt(token)
                if payload is None:
                    raise ValueError("Invalid or expired token")

                # Attach user info to request state
                request.state.user = payload

            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            request.state.user = None  # Anonymous request

        return await call_next(request)

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None