import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from loguru import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logger.info(f"➡️ {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)

        # Log response status and duration
        logger.info(f"⬅️ {request.method} path: {request.url.path}, status_code:{response.status_code}, process_time: {process_time} ms")

        return response
