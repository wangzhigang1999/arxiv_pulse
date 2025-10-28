"""arXiv API fetcher."""

from datetime import datetime

import feedparser
import requests


def fetch_arxiv_papers(url: str) -> list[dict]:
    """Fetch papers from arXiv API.

    Args:
        url: arXiv API URL

    Returns:
        List of paper dictionaries
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    feed = feedparser.parse(response.content)

    papers = []
    for entry in feed.entries:
        paper = {
            "id": entry.id.split("/")[-1],
            "title": entry.title,
            "summary": entry.summary,
            "authors": ", ".join([author.name for author in entry.authors]),
            "published": datetime(*entry.published_parsed[:6]),
            "updated": datetime(*entry.updated_parsed[:6]),
            "categories": ", ".join([tag.term for tag in entry.tags]),
            "link": entry.link,
        }
        papers.append(paper)

    return papers
