"""Audit schemas."""

from pydantic import BaseModel, Field


class AuditRequest(BaseModel):
    url: str


class AuditIssue(BaseModel):
    check: str
    severity: str = "warning"
    message: str


class AuditReport(BaseModel):
    url: str
    status_code: int
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    issues: list[AuditIssue] = Field(default_factory=list)
    title: str | None = None
    meta_description: str | None = None
    word_count: int = 0
