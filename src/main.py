from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.schemas.user import Dto
from src.api.v1.auth_route import AuthRoute
from src.api.v1.user_route import UserRoute
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.utils.middle_ware import SQLModelSessionMiddleware, LoggingMiddleware
from src.db.session import engine

app = FastAPI()
# Add middleware for DB session management
app.add_middleware(SQLModelSessionMiddleware, db_engine=engine)
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
