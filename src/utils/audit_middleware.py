from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError
from loguru import logger
from src.core.audit_context import current_user_email
from src.core.env_vars import secret_key, algorithm


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()

        if token:
            try:
                payload = jwt.decode(token, secret_key, algorithms=algorithm)
                email = payload.get("sub")
                if email:
                    logger.debug(f"[AUDIT] Setting current_user_email to: {email}")
                    current_user_email.set(email)
            except JWTError as e:
                logger.warning(f"[AUDIT] Invalid token: {str(e)}")
        else:
            logger.warning("[AUDIT] No Authorization token found")

        response = await call_next(request)
        return response
