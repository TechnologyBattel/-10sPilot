"""Keyword engine HTTP router (mounted at /api/v1/keywords)."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.modules.keyword_engine.cluster import cluster_keywords
from app.modules.keyword_engine.research import expand_keywords

router = APIRouter(prefix="/api/v1/keywords", tags=["keywords"])


class ExpandRequest(BaseModel):
    seed: str = Field(min_length=1)
    limit: int = Field(default=20, ge=1, le=100)
    country: str = "us"
    language: str = "en"


class ExpandResponse(BaseModel):
    seed: str
    keywords: list[str] = Field(default_factory=list)


class ClusterRequest(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    threshold: float = Field(default=0.25, ge=0.0, le=1.0)


class Cluster(BaseModel):
    name: str
    keywords: list[str]
    intent: str


class ClusterResponse(BaseModel):
    clusters: list[Cluster] = Field(default_factory=list)


@router.post("/expand", response_model=ExpandResponse)
async def expand(request: ExpandRequest) -> ExpandResponse:
    keywords = await expand_keywords(
        request.seed,
        limit=request.limit,
        country=request.country,
        language=request.language,
    )
    return ExpandResponse(seed=request.seed, keywords=keywords)


@router.post("/cluster", response_model=ClusterResponse)
def cluster(request: ClusterRequest) -> ClusterResponse:
    return ClusterResponse.model_validate(
        cluster_keywords(request.keywords, threshold=request.threshold)
    )
