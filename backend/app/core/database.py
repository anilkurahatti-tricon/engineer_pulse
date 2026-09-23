"""Centralized database connection and session management.

Provides:
- SQLAlchemy engine with connection pooling
- Scoped sessionmaker (SessionLocal)
- Declarative Base for ORM models
- FastAPI dependency generator `get_db()`
"""
from collections.abc import Generator
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize centralized SQLAlchemy Engine
# pool_pre_ping checks the connection liveness before handing it out from pool
engine = create_engine(
    settings.effective_database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Centralized session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and safely closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Verify active database connectivity and return True if successful."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning(f"Database connection check failed: {exc}")
        return False
