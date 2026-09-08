"""Keyword research and clustering endpoints."""

from fastapi import APIRouter, Request

from app.core.limiter import limiter
from app.modules.keyword_engine import (
    Keyword,
    KeywordCluster,
    KeywordResearchRequest,
    KeywordService,
)

# POST /api/v1/keywords/expand and /cluster live in app.modules.keyword_engine.router.

router = APIRouter()
service = KeywordService()


@router.post("/research", response_model=list[Keyword])
@limiter.limit("20/minute")
async def research(request: Request, payload: KeywordResearchRequest) -> list[Keyword]:
    return await service.research(payload)


@router.post("/clusters", response_model=list[KeywordCluster])
@limiter.limit("20/minute")
async def clusters(request: Request, payload: KeywordResearchRequest) -> list[KeywordCluster]:
    return await service.research_and_cluster(payload)
