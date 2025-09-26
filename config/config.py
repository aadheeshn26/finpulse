"""
Configuration module for FinPulse application.

This module manages application configuration including database settings,
API keys, and other environment-specific variables.
"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses Pydantic BaseSettings for automatic environment variable loading
    and validation.
    """
    
    # Database configuration
    database_url: str = "sqlite:///./finpulse.db"
    database_echo: bool = True  # Set to False in production
    
    # API Configuration
    api_title: str = "FinPulse API"
    api_description: str = "Financial Sentiment Analysis API"
    api_version: str = "1.0.0"
    debug: bool = True
    
    # Reddit API credentials (set via environment variables)
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: str = "FinPulse:v1.0.0 (by /u/yourredditusername)"
    
    # News API settings
    news_api_key: Optional[str] = None
    
    # Scraping settings
    max_articles_per_source: int = 1000
    max_reddit_posts_per_subreddit: int = 1000
    scraping_delay_seconds: float = 1.0  # Delay between requests
    
    # Sentiment analysis settings
    sentiment_models: list = ["vader", "textblob"]  # Available models
    default_sentiment_model: str = "vader"
    sentiment_threshold: float = 0.1  # Minimum sentiment strength to classify as positive/negative
    
    # Processing settings
    batch_size: int = 100  # Number of items to process at once
    max_workers: int = 4    # Number of parallel workers for processing
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "finpulse.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()


def get_database_url() -> str:
    """Get the database URL from settings."""
    return settings.database_url


def get_reddit_config() -> dict:
    """Get Reddit API configuration."""
    return {
        "client_id": settings.reddit_client_id,
        "client_secret": settings.reddit_client_secret,
        "user_agent": settings.reddit_user_agent
    }