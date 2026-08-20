"""Workflow schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    project: str
    domain: str
    seed_keyword: str
    url: str | None = None
    steps: list[str] = Field(default_factory=list)
    dry_run: bool = False


class WorkflowStepResult(BaseModel):
    step: str
    status: str = "succeeded"
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class WorkflowRun(BaseModel):
    project: str
    domain: str
    status: str = "succeeded"
    started_at: datetime
    finished_at: datetime | None = None
    steps: list[WorkflowStepResult] = Field(default_factory=list)
