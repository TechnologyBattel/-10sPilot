"""AEO schemas."""

from pydantic import BaseModel, Field


class AeoSignal(BaseModel):
    name: str
    passed: bool
    detail: str


class AeoReport(BaseModel):
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    signals: list[AeoSignal] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
