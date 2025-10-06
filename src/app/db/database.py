"""Database engine and session management."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from ..config import get_settings


def _create_engine():
    settings = get_settings()
    return create_engine(settings.database_url, echo=settings.debug, future=True)


_ENGINE = _create_engine()


def get_engine():  # pragma: no cover - thin wrapper used for dependency injection
    return _ENGINE


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Provide a context-managed SQLModel session."""

    with Session(_ENGINE) as session:
        yield session


def init_db() -> None:
    """Create database tables if they do not exist."""

    from . import models  # noqa: F401  Ensures model metadata is registered

    SQLModel.metadata.create_all(_ENGINE)


__all__ = ["get_engine", "get_session", "init_db"]
