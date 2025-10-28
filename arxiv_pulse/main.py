"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from arxiv_pulse.database import init_db
from arxiv_pulse.scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.error("Please ensure MySQL is running and database URL is correct")
        raise

    scheduler = setup_scheduler()
    logger.info("arXiv Pulse scheduler started")
    yield
    scheduler.shutdown()
    logger.info("arXiv Pulse scheduler stopped")


app = FastAPI(title="arXiv Pulse", lifespan=lifespan)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "arXiv Pulse API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


def main():
    """Main entry point."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
