"""Keyword research and clustering endpoints."""

from fastapi import APIRouter

from app.modules.keyword_engine import (
    Keyword,
    KeywordCluster,
    KeywordResearchRequest,
    KeywordService,
)

router = APIRouter()
service = KeywordService()


@router.post("/research", response_model=list[Keyword])
async def research(request: KeywordResearchRequest) -> list[Keyword]:
    return await service.research(request)


@router.post("/clusters", response_model=list[KeywordCluster])
async def clusters(request: KeywordResearchRequest) -> list[KeywordCluster]:
    return await service.research_and_cluster(request)


@router.post("/cluster", response_model=list[KeywordCluster])
def cluster(keywords: list[Keyword]) -> list[KeywordCluster]:
    return service.cluster(keywords)
