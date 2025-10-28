"""Scheduler for periodic arXiv crawls."""

import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from arxiv_pulse.database import SessionLocal, settings
from arxiv_pulse.fetcher import fetch_arxiv_papers_by_category
from arxiv_pulse.models import ArxivPaper


def crawl_arxiv():
    """Crawl arXiv and store papers in database."""
    try:
        logger.info(f"Crawling arXiv at {datetime.datetime.now()}")
        logger.info(f"Categories: {settings.arxiv_categories}")

        categories_list = [cat.strip() for cat in settings.arxiv_categories.split(",")]
        all_papers = []

        for category in categories_list:
            papers = fetch_arxiv_papers_by_category(
                category=category,
                max_results=50,
                page_size=settings.arxiv_page_size,
            )
            all_papers.extend(papers)

        logger.info(f"Total papers fetched: {len(all_papers)}")

        unique_papers = {}
        for paper in all_papers:
            unique_papers[paper["id"]] = paper

        logger.info(f"Unique papers after deduplication: {len(unique_papers)}")

        db = SessionLocal()

        paper_ids = list(unique_papers.keys())
        existing_ids = set(
            db.query(ArxivPaper.id).filter(ArxivPaper.id.in_(paper_ids)).all()
        )
        existing_ids = {row[0] for row in existing_ids}

        logger.info(f"Found {len(existing_ids)} existing papers in database")

        added_count = 0
        error_count = 0

        for paper_data in unique_papers.values():
            if paper_data["id"] not in existing_ids:
                try:
                    paper = ArxivPaper(**paper_data)
                    db.add(paper)
                    added_count += 1
                except Exception as e:
                    logger.warning(f"Failed to add paper {paper_data['id']}: {e}")
                    error_count += 1

        try:
            db.commit()
            logger.success(f"Successfully committed {added_count} papers to database")
        except Exception as e:
            logger.error(f"Failed to commit to database: {e}")
            db.rollback()
            raise

        db.close()

        logger.info(
            f"Crawled {len(all_papers)} papers, deduplicated to {len(unique_papers)}, "
            f"added {added_count} new papers, {error_count} errors"
        )
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
