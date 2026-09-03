from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import Project


def test_project_crud_integration() -> None:
    engine = create_engine(settings.database_url)

    with Session(engine) as db:
        project = Project(
            name="DB Integration Test",
            domain="db-integration-test.example",
            country="US",
            language="en",
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        assert project.id is not None
        project_id = project.id

        found = db.scalar(
            select(Project).where(Project.id == project_id)
        )

        assert found is not None
        assert found.name == "DB Integration Test"
        assert found.domain == "db-integration-test.example"

        db.delete(found)
        db.commit()

        remaining = db.scalar(
            select(Project).where(Project.id == project_id)
        )

        assert remaining is None

    engine.dispose()
