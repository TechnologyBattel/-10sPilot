"""FastAPI application entrypoint."""

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.api.v1.routes import health
from app.core.config import settings
from app.core.limiter import limiter
from app.modules.aeo_engine.router import router as aeo_router
from app.modules.audit_engine.router import router as audit_router
from app.modules.keyword_engine.router import router as keyword_router
from app.modules.serp_engine.router import router as serp_router


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, version=settings.version)
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type"],
    )
    application.include_router(health.router, tags=["health"])
    application.include_router(api_router, prefix="/api/v1")
    application.include_router(serp_router)
    application.include_router(keyword_router)
    application.include_router(aeo_router)
    application.include_router(audit_router)
    return application

app = create_app()
