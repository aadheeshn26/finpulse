"""
Article model for storing financial news articles.

This model represents financial news articles scraped from various sources
like Yahoo Finance, Reuters, Bloomberg, etc.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Article(Base):
    """
    Represents a financial news article.
    
    This model stores the core information about financial news articles
    including metadata like source, publication date, and content.
    """
    
    __tablename__ = "articles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Article metadata
    title = Column(String(500), nullable=False, index=True)
    url = Column(String(1000), unique=True, nullable=False, index=True)
    source = Column(String(100), nullable=False, index=True)  # e.g., "Yahoo Finance", "Reuters"
    author = Column(String(200), nullable=True)
    
    # Content
    content = Column(Text, nullable=False)  # Full article text
    summary = Column(Text, nullable=True)   # Article summary if available
    
    # Timestamps
    published_at = Column(DateTime, nullable=False, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Financial context
    ticker_symbols = Column(String(500), nullable=True)  # Comma-separated list: "AAPL,MSFT,GOOGL"
    market_sector = Column(String(100), nullable=True)   # e.g., "Technology", "Healthcare"
    
    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False)
    processing_error = Column(Text, nullable=True)
    
    # Content metrics
    word_count = Column(Integer, nullable=True)
    reading_time_minutes = Column(Float, nullable=True)
    
    # Relationships
    sentiment_scores = relationship("SentimentScore", back_populates="article", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:50]}...', source='{self.source}')>"
    
    def __str__(self):
        return f"{self.title} - {self.source} ({self.published_at.strftime('%Y-%m-%d')})"