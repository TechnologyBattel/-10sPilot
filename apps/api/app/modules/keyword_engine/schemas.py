"""Keyword engine schemas."""

from pydantic import BaseModel, Field


class KeywordResearchRequest(BaseModel):
    seed: str
    domain: str | None = None
    country: str = "us"
    limit: int = Field(default=20, ge=1, le=200)


class Keyword(BaseModel):
    term: str
    intent: str = "informational"
    difficulty: float = Field(default=0.0, ge=0.0, le=100.0)
    opportunity: float = Field(default=0.0, ge=0.0, le=100.0)
    source: str = "serp"


class KeywordCluster(BaseModel):
    label: str
    keywords: list[Keyword] = Field(default_factory=list)
