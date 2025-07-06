import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


class SQLModelSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db_engine):
        super().__init__(app)
        self.engine = db_engine

    async def dispatch(self, request: Request, call_next):
        request.state.db = Session(self.engine)
        try:
            response = await call_next(request)
            request.state.db.commit()
        except SQLAlchemyError:
            request.state.db.rollback()
            raise
        finally:
            request.state.db.close()
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logger.info(f"➡️ {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)

        # Log response status and duration
        logger.info(f"⬅️ {request.method} {request.url.path}, status_code: {response.status_code}, process time: ({process_time} ms)")

        return response
