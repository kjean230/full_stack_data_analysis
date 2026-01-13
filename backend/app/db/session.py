from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # validates connections before using (helps with MySQL restarts)
    pool_recycle=3600,    # avoid stale MySQL connections
    echo=False,           # keep False; we’ll add controlled SQL logging later
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a DB session and guarantees cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()