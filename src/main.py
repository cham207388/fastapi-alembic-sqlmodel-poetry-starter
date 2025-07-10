from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from src.core.events import init_events
from src.api.v1.auth_route import AuthRoute
from src.api.v1.user_route import UserRoute
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.utils.audit_middleware import AuditMiddleware
from src.utils.logging_middleware import LoggingMiddleware
from src.utils.sql_middleware import SQLModelSessionMiddleware
from src.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_events()  # ✅ register audit listeners here
    yield
app = FastAPI(lifespan=lifespan)
# Add middleware for DB session management
app.add_middleware(SQLModelSessionMiddleware, db_engine=engine)
app.add_middleware(LoggingMiddleware)
# Then audit middleware (after DB session is available)
app.add_middleware(AuditMiddleware)

# Create instrumentation instance
instrumentation = Instrumentator().instrument(app).expose(app)

auth_service = AuthService()
user_service = UserService(auth_service)
user_route = UserRoute(user_service)
auth_route = AuthRoute(auth_service)

app.include_router(auth_route.router)
app.include_router(user_route.router)
