"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.api.v1.routes import health
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, version=settings.version)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health.router, tags=["health"])
    application.include_router(api_router, prefix="/api/v1")
    return application


app = create_app()
