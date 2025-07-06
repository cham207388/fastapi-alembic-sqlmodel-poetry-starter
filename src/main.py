from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.dao.schemas import Dto
from src.route.auth_route import AuthRoute
from src.route.user_route import UserRoute
from src.service.auth_service import AuthService
from src.service.user_service import UserService
from src.util.middle_ware import SQLModelSessionMiddleware, LoggingMiddleware
from src.dao.db import engine

app = FastAPI()
# Add middleware for DB session management
app.add_middleware(SQLModelSessionMiddleware, db_engine=engine)

# Add logging middleware
app.add_middleware(LoggingMiddleware)
# Create instrumentation instance
instrumentation = Instrumentator().instrument(app).expose(app)

auth_service = AuthService()
dto = Dto()
user_service = UserService(auth_service, dto)
user_route = UserRoute(user_service)
auth_route = AuthRoute(auth_service)

app.include_router(auth_route.router)
app.include_router(user_route.router)
