"""Database connection setup for MVP.

This module provides:
- SQLite connection URL
- SQLAlchemy engine
- SessionLocal factory
- Declarative Base
- `init_db()` helper
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./python_learning_mvp.db"

# SQLite needs `check_same_thread=False` for multi-threaded environments (e.g. Streamlit).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    """Initialize database schema for all registered SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
