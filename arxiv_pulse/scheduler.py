"""Scheduler for periodic arXiv crawls."""

import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from arxiv_pulse.database import SessionLocal, settings
from arxiv_pulse.fetcher import fetch_arxiv_papers
from arxiv_pulse.models import ArxivPaper

logger = logging.getLogger(__name__)

ARXIV_URL = (
    "https://export.arxiv.org/api/query"
    "?search_query=cat:cs.AI"
    "&sortBy=submittedDate"
    "&sortOrder=descending"
    "&start=0"
    "&max_results=100"
)


def crawl_arxiv():
    """Crawl arXiv and store papers in database."""
    try:
        logger.info(f"Crawling arXiv at {datetime.datetime.now()}")
        papers = fetch_arxiv_papers(ARXIV_URL)
        db = SessionLocal()

        added_count = 0
        for paper_data in papers:
            existing = (
                db.query(ArxivPaper).filter(ArxivPaper.id == paper_data["id"]).first()
            )
            if not existing:
                paper = ArxivPaper(**paper_data)
                db.add(paper)
                added_count += 1

        db.commit()
        db.close()

        logger.info(f"Crawled {len(papers)} papers, added {added_count} new papers")
    except Exception as e:
        logger.error(f"Error crawling arXiv: {e}")


def setup_scheduler():
    """Setup and start the scheduler."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        crawl_arxiv,
        trigger=IntervalTrigger(minutes=settings.crawl_interval_minutes),
        id="arxiv_crawl",
        replace_existing=True,
    )
    scheduler.start()

    logger.info("Starting initial crawl...")
    crawl_arxiv()

    return scheduler
