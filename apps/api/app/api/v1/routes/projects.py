from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.core.limiter import limiter
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import (
    create_project,
    delete_project,
    get_project,
    list_projects,
)

router = APIRouter()

DbSession = Annotated[Session, Depends(db_session)]


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
def create(
    request: Request,
    data: ProjectCreate,
    db: DbSession,
) -> ProjectResponse:
    return create_project(db, data)


@router.get("", response_model=list[ProjectResponse])
@limiter.limit("60/minute")
def list_all(
    request: Request,
    db: DbSession,
) -> list[ProjectResponse]:
    return list_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
@limiter.limit("60/minute")
def get_one(
    request: Request,
    project_id: str,
    db: DbSession,
) -> ProjectResponse:
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
def delete(
    request: Request,
    project_id: str,
    db: DbSession,
) -> None:
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    delete_project(db, project)
