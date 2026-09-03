"""Project API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    domain: str = Field(min_length=1, max_length=255)
    country: str = Field(default="us", min_length=2, max_length=2)
    language: str = Field(default="en", min_length=2, max_length=10)
    gsc_site_url: str | None = Field(default=None, max_length=500)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    domain: str
    country: str
    language: str
    gsc_site_url: str | None
    created_at: datetime
    updated_at: datetime
