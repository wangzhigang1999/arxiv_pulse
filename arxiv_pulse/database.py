"""Database configuration and session management."""

import logging

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "mysql+pymysql://root:password@localhost:3306/arxiv_pulse"
    crawl_interval_minutes: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
Base = declarative_base()

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to initialize database: {e}")
        raise
