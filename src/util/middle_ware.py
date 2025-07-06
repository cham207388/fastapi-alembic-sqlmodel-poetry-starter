from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

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