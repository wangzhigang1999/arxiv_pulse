"""Database models."""

from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from arxiv_pulse.database import Base


class ArxivPaper(Base):
    """arXiv paper model."""

    __tablename__ = "arxiv_papers"

    id = Column(String(50), primary_key=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    authors = Column(Text)
    published = Column(DateTime)
    updated = Column(DateTime)
    categories = Column(String(200))
    link = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
