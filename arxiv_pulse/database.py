"""Database configuration and session management."""

from loguru import logger
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "mysql+pymysql://root:password@localhost:3306/arxiv_pulse"
    crawl_interval_minutes: int = 60
    arxiv_categories: str = (
        "cs.AI,cs.CV,cs.LG,cs.CL,cs.NE,cs.SE,cs.DC,cs.DS,"
        "cs.DB,cs.IR,cs.ET,cs.GL,cs.IT,cs.MA"
    )
    arxiv_page_size: int = 100

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
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
