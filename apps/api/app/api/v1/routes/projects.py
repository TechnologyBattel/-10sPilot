"""Project API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import (
    create_project,
    delete_project,
    get_project,
    list_projects,
)

router = APIRouter()


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: ProjectCreate,
    db: Session = Depends(db_session),
) -> ProjectResponse:
    return create_project(db, data)


@router.get("", response_model=list[ProjectResponse])
def list_all(
    db: Session = Depends(db_session),
) -> list[ProjectResponse]:
    return list_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_one(
    project_id: str,
    db: Session = Depends(db_session),
) -> ProjectResponse:
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    project_id: str,
    db: Session = Depends(db_session),
) -> None:
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    delete_project(db, project)
