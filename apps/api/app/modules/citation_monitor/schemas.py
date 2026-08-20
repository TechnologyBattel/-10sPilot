"""Citation monitor schemas."""

from pydantic import BaseModel, Field


class CitationRequest(BaseModel):
    prompt: str
    domain: str
    brand: str | None = None
    engines: list[str] = Field(default_factory=lambda: ["chatgpt", "perplexity", "gemini"])


class CitationCheck(BaseModel):
    engine: str
    prompt: str
    cited: bool = False
    mentioned: bool = False
    position: int | None = None
    answer_excerpt: str = ""
    error: str | None = None
