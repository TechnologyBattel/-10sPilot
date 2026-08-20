"""Shared FastAPI dependencies."""

from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.db.session import get_db


def db_session() -> Iterator[Session]:
    yield from get_db()
