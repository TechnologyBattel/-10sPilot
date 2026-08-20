"""Content engine schemas."""

from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    keyword: str
    domain: str | None = None
    tone: str = "expert, concise"
    word_count: int = Field(default=900, ge=200, le=4000)


class ContentBrief(BaseModel):
    keyword: str
    title: str
    outline: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)


class ContentDraft(BaseModel):
    keyword: str
    title: str
    markdown: str
    aeo_score: float = 0.0
    geo_score: float = 0.0
    word_count: int = 0
