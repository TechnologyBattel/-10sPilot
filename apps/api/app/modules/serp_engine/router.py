"""SERP engine HTTP router (mounted at /api/v1/serp)."""

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.modules.serp_engine.free_serp import get_serp_results

router = APIRouter(prefix="/api/v1/serp", tags=["serp"])


class SerpSearchRequest(BaseModel):
    keyword: str = Field(min_length=1)
    domain: str | None = None
    country: str = "us"
    language: str = "en"
    num_results: int = Field(default=10, ge=1, le=100)


class SerpSearchResult(BaseModel):
    position: int
    title: str
    url: str
    snippet: str | None = None


class SerpSearchResponse(BaseModel):
    keyword: str
    domain: str | None = None
    results: list[SerpSearchResult] = Field(default_factory=list)
    domain_position: int | None = None


def _domain_position(results: list[dict[str, Any]], domain: str | None) -> int | None:
    if not domain:
        return None
    target = domain.removeprefix("https://").removeprefix("http://").removeprefix("www.").strip("/")
    for item in results:
        url = str(item.get("url", ""))
        host = url.split("//")[-1].split("/")[0].removeprefix("www.")
        if host == target:
            return int(item["position"])
    return None


@router.post("/search", response_model=SerpSearchResponse)
async def search(request: SerpSearchRequest) -> SerpSearchResponse:
    results = await get_serp_results(
        request.keyword,
        num_results=request.num_results,
        country=request.country,
        language=request.language,
    )
    return SerpSearchResponse(
        keyword=request.keyword,
        domain=request.domain,
        results=[SerpSearchResult.model_validate(item) for item in results],
        domain_position=_domain_position(results, request.domain),
    )
