"""
Reddit post model for storing financial discussion posts.

This model represents Reddit posts from financial subreddits like
r/wallstreetbets, r/investing, r/stocks, etc.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class RedditPost(Base):
    """
    Represents a Reddit post from financial discussion subreddits.
    
    This model stores Reddit posts and comments that discuss financial
    topics, stocks, market trends, etc.
    """
    
    __tablename__ = "reddit_posts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Reddit-specific identifiers
    reddit_id = Column(String(50), unique=True, nullable=False, index=True)  # Reddit's post ID
    reddit_url = Column(String(500), nullable=False)
    
    # Post metadata
    title = Column(String(300), nullable=False, index=True)
    subreddit = Column(String(50), nullable=False, index=True)  # e.g., "wallstreetbets", "investing"
    author = Column(String(100), nullable=True)  # Reddit username
    
    # Content
    content = Column(Text, nullable=True)  # Post body (can be None for link posts)
    post_type = Column(String(20), nullable=False)  # "text", "link", "image", "video"
    
    # Engagement metrics
    score = Column(Integer, default=0, nullable=False)  # Upvotes - downvotes
    upvote_ratio = Column(Float, nullable=True)  # Reddit's upvote ratio
    num_comments = Column(Integer, default=0, nullable=False)
    num_crossposts = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, index=True)  # When post was created on Reddit
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Financial context
    ticker_symbols = Column(String(500), nullable=True)  # Mentioned stock symbols
    flair = Column(String(100), nullable=True)  # Reddit post flair (e.g., "DD", "YOLO", "Discussion")
    
    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False)
    processing_error = Column(Text, nullable=True)
    
    # Content analysis
    word_count = Column(Integer, nullable=True)
    contains_positions = Column(Boolean, default=False, nullable=False)  # Does post mention stock positions?
    mention_count = Column(Integer, default=0, nullable=False)  # How many stock symbols mentioned
    
    # Moderation status
    is_removed = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    is_nsfw = Column(Boolean, default=False, nullable=False)
    is_spoiler = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    sentiment_scores = relationship("SentimentScore", back_populates="reddit_post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<RedditPost(id={self.id}, reddit_id='{self.reddit_id}', subreddit='r/{self.subreddit}')>"
    
    def __str__(self):
        return f"r/{self.subreddit}: {self.title[:50]}... (Score: {self.score})"