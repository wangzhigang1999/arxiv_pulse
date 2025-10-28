"""arXiv API fetcher using official arxiv library."""

import arxiv
from loguru import logger


def fetch_arxiv_papers_by_category(
    category: str,
    max_results: int = 200,
    page_size: int = 100,
) -> list[dict]:
    """Fetch latest papers from arXiv for a single category.

    Sorted by submission date descending (newest first).

    Args:
        category: Single category (e.g., "cs.AI")
        max_results: Maximum number of results per category
        page_size: Number of results per API request (max 2000)

    Returns:
        List of paper dictionaries
    """
    logger.info(f"Fetching papers from category: {category}")

    search_query = f"cat:{category}"
    logger.debug(f"Search query: {search_query}")

    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    client = arxiv.Client(page_size=page_size)
    papers = []
    try:
        for _idx, result in enumerate(client.results(search), 1):
            paper = {
                "id": result.entry_id.split("/")[-1],
                "title": result.title,
                "summary": result.summary,
                "authors": ", ".join([author.name for author in result.authors]),
                "published": result.published,
                "updated": result.updated,
                "categories": ", ".join(result.categories),
                "link": result.entry_id,
            }
            papers.append(paper)

        logger.success(f"Successfully fetched {len(papers)} papers from {category}")
    except Exception as e:
        logger.error(f"Failed to fetch papers from {category}: {e}")
        return []

    return papers
