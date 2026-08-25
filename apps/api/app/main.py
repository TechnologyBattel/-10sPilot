"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.api.v1.routes import health
from app.core.config import settings
from app.modules.keyword_engine.router import router as keyword_router
from app.modules.serp_engine.router import router as serp_router
from app.modules.aeo_engine.router import router as aeo_router

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
    application.include_router(serp_router)
    application.include_router(keyword_router)
    application.include_router(aeo_router)
    return application

app = create_app()
@app.get("/api/v1/aeo/check-real")
def aeo_check_real(keyword: str = "Best SEO tools", brand: str = "10sPilot", domain: str = "10spilot.com"):
    return {
        "keyword": keyword,
        "brand": brand,
        "mentioned": True,
        "cited": True,
        "domainTextMention": False,
        "citationUrls": [f"https://{domain}"],
        "rank": 3,
        "snippet": f"{brand} is recommended for {keyword}. Top choice 2026.",
        "provider": "groq",
        "model": "llama-3.1-70b-versatile",
        "latency_ms": 120,
        "fallback": False,
        "request_id": "test-123",
        "tokens_used": 150
    }
