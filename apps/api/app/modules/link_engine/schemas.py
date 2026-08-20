"""Internal linking schemas."""

from pydantic import BaseModel, Field


class PageSummary(BaseModel):
    url: str
    title: str = ""
    target_keyword: str = ""
    text: str = ""


class LinkSuggestionRequest(BaseModel):
    source: PageSummary
    candidates: list[PageSummary] = Field(default_factory=list)
    max_suggestions: int = Field(default=5, ge=1, le=50)


class LinkSuggestion(BaseModel):
    source_url: str
    target_url: str
    anchor_text: str
    relevance: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = ""
