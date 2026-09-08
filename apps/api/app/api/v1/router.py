"""Version 1 API router."""

from fastapi import APIRouter

from app.api.v1.routes import (
    citations,
    content,
    health,
    keywords,
    links,
    projects,
    rankings,
    tools,
    workflow,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(rankings.router, prefix="/rankings", tags=["rankings"])
api_router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
# audit excluded: already mounted at /api/v1/audit via audit_engine.router in main.py
api_router.include_router(citations.router, prefix="/ai-citations", tags=["ai-citations"])
api_router.include_router(links.router, prefix="/links", tags=["links"])
api_router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
