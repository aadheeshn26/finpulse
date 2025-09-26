"""
Data collection and web scraping package.

This package contains scrapers for financial news websites,
Reddit posts, and other data sources.
"""

from .news_scraper import NewsArticleScraper
from .reddit_scraper import RedditScraper
from .base_scraper import BaseScraper

__all__ = [
    "BaseScraper",
    "NewsArticleScraper", 
    "RedditScraper"
]