"""SQLAlchemy persistence models for 10sPilot."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


def new_id() -> str:
    """Generate an application-level string identifier."""
    return uuid.uuid4().hex


def utc_now() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    from datetime import timezone

    return datetime.now(timezone.utc)


class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"


class WorkflowStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class SearchIntent(str, enum.Enum):
    INFORMATIONAL = "informational"
    COMMERCIAL = "commercial"
    TRANSACTIONAL = "transactional"
    NAVIGATIONAL = "navigational"


class AiEngine(str, enum.Enum):
    CHATGPT = "chatgpt"
    PERPLEXITY = "perplexity"
    GEMINI = "gemini"
    COPILOT = "copilot"
    AI_OVERVIEWS = "ai_overviews"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String(2), nullable=False, default="us")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    gsc_site_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    keywords: Mapped[list[Keyword]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    clusters: Mapped[list[KeywordCluster]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    contents: Mapped[list[Content]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    audits: Mapped[list[Audit]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    rankings: Mapped[list[Ranking]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    ai_citations: Mapped[list[AiCitation]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    workflow_runs: Mapped[list[WorkflowRun]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class KeywordCluster(Base):
    __tablename__ = "keyword_clusters"
    __table_args__ = (
        UniqueConstraint("project_id", "label", name="uq_keyword_cluster_project_label"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    pillar_topic: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    project: Mapped[Project] = relationship(back_populates="clusters")
    keywords: Mapped[list[Keyword]] = relationship(back_populates="cluster")


class Keyword(Base):
    __tablename__ = "keywords"
    __table_args__ = (
        UniqueConstraint("project_id", "term", name="uq_keyword_project_term"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    term: Mapped[str] = mapped_column(String(500), nullable=False)
    intent: Mapped[SearchIntent] = mapped_column(
        default=SearchIntent.INFORMATIONAL, nullable=False
    )
    difficulty: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    opportunity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="serp")
    cluster_id: Mapped[str | None] = mapped_column(
        ForeignKey("keyword_clusters.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    project: Mapped[Project] = relationship(back_populates="keywords")
    cluster: Mapped[KeywordCluster | None] = relationship(back_populates="keywords")
    contents: Mapped[list[Content]] = relationship(back_populates="keyword")
    rankings: Mapped[list[Ranking]] = relationship(back_populates="keyword")


class Content(Base):
    __tablename__ = "contents"
    __table_args__ = (
        UniqueConstraint("project_id", "slug", name="uq_content_project_slug"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    keyword_id: Mapped[str | None] = mapped_column(
        ForeignKey("keywords.id", ondelete="SET NULL"), nullable=True, index=True
    )
    cluster_id: Mapped[str | None] = mapped_column(
        ForeignKey("keyword_clusters.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    slug: Mapped[str] = mapped_column(String(500), nullable=False)
    markdown: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ContentStatus] = mapped_column(
        default=ContentStatus.DRAFT, nullable=False
    )
    aeo_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    geo_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    word_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    project: Mapped[Project] = relationship(back_populates="contents")
    keyword: Mapped[Keyword | None] = relationship(back_populates="contents")
    cluster: Mapped[KeywordCluster | None] = relationship()


class Audit(Base):
    __tablename__ = "audits"
    __table_args__ = (
        Index("ix_audits_project_url", "project_id", "url"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    url: Mapped[str] = mapped_column(String(2000), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    issues: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    project: Mapped[Project] = relationship(back_populates="audits")


class Ranking(Base):
    __tablename__ = "rankings"
    __table_args__ = (
        Index("ix_rankings_keyword_checked_at", "keyword_id", "checked_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    keyword_id: Mapped[str] = mapped_column(
        ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True
    )
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    impressions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="serper")
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, index=True
    )

    project: Mapped[Project] = relationship(back_populates="rankings")
    keyword: Mapped[Keyword] = relationship(back_populates="rankings")


class AiCitation(Base):
    __tablename__ = "ai_citations"
    __table_args__ = (
        Index(
            "ix_ai_citations_project_engine_checked_at",
            "project_id",
            "engine",
            "checked_at",
        ),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    engine: Mapped[AiEngine] = mapped_column(nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    cited: Mapped[bool] = mapped_column(nullable=False, default=False)
    mentioned: Mapped[bool] = mapped_column(nullable=False, default=False)
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answer_excerpt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, index=True
    )

    project: Mapped[Project] = relationship(back_populates="ai_citations")


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    __table_args__ = (
        Index("ix_workflow_runs_project_started_at", "project_id", "started_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    workflow: Mapped[str] = mapped_column(String(100), nullable=False, default="full_pilot")
    status: Mapped[WorkflowStatus] = mapped_column(
        default=WorkflowStatus.QUEUED, nullable=False
    )
    steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, index=True
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    project: Mapped[Project] = relationship(back_populates="workflow_runs")
