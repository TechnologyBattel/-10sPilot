"""SERP engine schemas."""

from pydantic import BaseModel, Field


class SerpQuery(BaseModel):
    keyword: str
    domain: str | None = None
    country: str = "us"
    language: str = "en"
    num_results: int = Field(default=10, ge=1, le=100)


class SerpResult(BaseModel):
    position: int
    title: str
    link: str
    snippet: str | None = None


class RankingResult(BaseModel):
    keyword: str
    domain: str | None = None
    position: int | None = None
    url: str | None = None
    results: list[SerpResult] = Field(default_factory=list)
    source: str = "serper"


class GscRow(BaseModel):
    query: str
    page: str | None = None
    clicks: int = 0
    impressions: int = 0
    ctr: float = 0.0
    position: float = 0.0
