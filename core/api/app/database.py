"""SQLModel database utilities."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

settings = get_settings()
connect_args: dict[str, object] = {}
engine_kwargs: dict[str, object] = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    if "file:" in settings.database_url:
        connect_args["uri"] = True
    if settings.database_url in {"sqlite://", "sqlite:///:memory:"} or "mode=memory" in settings.database_url:
        engine_kwargs["poolclass"] = StaticPool
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args, **engine_kwargs)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
