"""Keyword research and clustering endpoints."""

from fastapi import APIRouter

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
async def research(request: KeywordResearchRequest) -> list[Keyword]:
    return await service.research(request)


@router.post("/clusters", response_model=list[KeywordCluster])
async def clusters(request: KeywordResearchRequest) -> list[KeywordCluster]:
    return await service.research_and_cluster(request)
