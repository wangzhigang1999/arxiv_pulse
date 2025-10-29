"""Scheduler for periodic arXiv crawls."""

import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from arxiv_pulse.database import SessionLocal, settings
from arxiv_pulse.dingtalk_service import dingtalk_service
from arxiv_pulse.fetcher import fetch_arxiv_papers_by_category
from arxiv_pulse.models import ArxivPaper
from arxiv_pulse.summary_generator import summary_generator


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
        existing_ids = set(db.query(ArxivPaper.id).filter(ArxivPaper.id.in_(paper_ids)).all())
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


def process_keyword_matches():
    """Process papers that match keywords, generate summaries and send notifications."""
    try:
        logger.info("Processing keyword-matched papers for summaries and notifications")

        # Parse keywords
        keywords = [kw.strip() for kw in settings.keywords.split(",") if kw.strip()]
        if not keywords:
            logger.warning("No keywords configured for monitoring")
            return

        db = SessionLocal()

        # Calculate one month ago
        one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)

        # Find papers that match keywords in both title and summary,
        # but don't have Chinese summaries yet. Only process papers from the last month
        query = db.query(ArxivPaper).filter(ArxivPaper.chinese_summary.is_(None), ArxivPaper.published >= one_month_ago)

        papers = query.all()
        logger.info(f"Found {len(papers)} papers without Chinese summaries")

        processed_count = 0
        summary_count = 0
        notification_count = 0

        for paper in papers:
            # Check if both title and summary contain keywords
            title_match = any(kw.lower() in paper.title.lower() for kw in keywords)
            summary_match = any(kw.lower() in paper.summary.lower() for kw in keywords)

            if title_match or summary_match:
                logger.info(f"Processing paper: {paper.title[:50]}...")

                # Generate Chinese summary
                chinese_summary = summary_generator.generate_chinese_summary(paper.title, paper.summary)

                if chinese_summary:
                    # Update paper with Chinese summary
                    paper.chinese_summary = chinese_summary
                    summary_count += 1

                    # Send DingTalk notification
                    paper_data = {
                        "title": paper.title,
                        "chinese_summary": chinese_summary,
                        "authors": paper.authors,
                        "link": paper.link,
                        "published": paper.published.strftime("%Y-%m-%d %H:%M:%S") if paper.published else "Unknown",
                    }

                    if dingtalk_service.send_paper_notification(paper_data):
                        notification_count += 1

                processed_count += 1

        # Commit all changes
        try:
            db.commit()
            logger.success(
                f"Processed {processed_count} papers, generated {summary_count} "
                f"summaries, sent {notification_count} notifications"
            )
        except Exception as e:
            logger.error(f"Failed to commit changes: {e}")
            db.rollback()
            raise

        db.close()

    except Exception as e:
        logger.error(f"Error processing keyword matches: {e}")


def setup_scheduler():
    """Setup and start the scheduler."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        crawl_arxiv,
        trigger=IntervalTrigger(minutes=settings.crawl_interval_minutes),
        id="arxiv_crawl",
        replace_existing=True,
    )

    # Add keyword processing job
    scheduler.add_job(
        process_keyword_matches,
        trigger=IntervalTrigger(minutes=settings.summary_interval_minutes),
        id="keyword_processing",
        replace_existing=True,
    )

    scheduler.start()
    process_keyword_matches()

    logger.info("Starting initial crawl...")
    crawl_arxiv()

    logger.info("Starting initial keyword processing...")

    return scheduler
