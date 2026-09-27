"""
SQLAlchemy engine + session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL
from bot.db.models import Base


engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new session (caller must close)."""
    return SessionLocal()
