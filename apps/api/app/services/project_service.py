"""Project persistence service."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Project
from app.schemas.project import ProjectCreate


def create_project(db: Session, data: ProjectCreate) -> Project:
    project = Project(
        name=data.name,
        domain=data.domain,
        country=data.country,
        language=data.language,
        gsc_site_url=data.gsc_site_url,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session) -> list[Project]:
    return list(
        db.scalars(
            select(Project).order_by(Project.created_at.desc())
        ).all()
    )


def get_project(db: Session, project_id: str) -> Project | None:
    return db.scalar(
        select(Project).where(Project.id == project_id)
    )


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
