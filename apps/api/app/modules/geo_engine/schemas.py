"""GEO schemas."""

from pydantic import BaseModel, Field


class GeoSignal(BaseModel):
    name: str
    passed: bool
    detail: str


class GeoReport(BaseModel):
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    signals: list[GeoSignal] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
