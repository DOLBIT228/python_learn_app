"""Database initialization and session management.

This module configures SQLite + SQLAlchemy primitives used by the rest of the
application. Models are intentionally not defined here.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# SQLite database file for local MVP development.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "app.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# SQLAlchemy engine configuration.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Factory for database sessions.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base class for declarative SQLAlchemy models.
Base = declarative_base()


def init_db() -> None:
    """Initialize database schema for all registered models.

    Note: Model definitions are not added yet. This function is prepared for
    future use once models are implemented and imported before metadata create.
    """

    Base.metadata.create_all(bind=engine)
