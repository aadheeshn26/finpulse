"""
Pydantic schemas for data validation and API serialization.

These schemas define the data structures for API requests and responses,
ensuring type safety and automatic validation.
"""

from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum


class SentimentLabel(str, Enum):
    """Enumeration for sentiment labels."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class MarketDirection(str, Enum):
    """Enumeration for market direction indicators."""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class PostType(str, Enum):
    """Enumeration for Reddit post types."""
    TEXT = "text"
    LINK = "link"
    IMAGE = "image"
    VIDEO = "video"


# Base schemas for common fields
class BaseTimestamp(BaseModel):
    """Base model with timestamp fields."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Article schemas
class ArticleBase(BaseModel):
    """Base schema for Article with common fields."""
    title: str = Field(..., min_length=1, max_length=500, description="Article title")
    url: HttpUrl = Field(..., description="Article URL")
    source: str = Field(..., min_length=1, max_length=100, description="News source")
    author: Optional[str] = Field(None, max_length=200, description="Article author")
    content: str = Field(..., min_length=10, description="Full article content")
    summary: Optional[str] = Field(None, description="Article summary")
    published_at: datetime = Field(..., description="Publication timestamp")
    ticker_symbols: Optional[str] = Field(None, max_length=500, description="Comma-separated ticker symbols")
    market_sector: Optional[str] = Field(None, max_length=100, description="Market sector")
    
    @validator('ticker_symbols')
    def validate_ticker_symbols(cls, v):
        """Validate ticker symbols format."""
        if v is not None:
            # Convert to uppercase and validate format
            symbols = [s.strip().upper() for s in v.split(',') if s.strip()]
            return ','.join(symbols) if symbols else None
        return v


class ArticleCreate(ArticleBase):
    """Schema for creating a new article."""
    pass


class ArticleUpdate(BaseModel):
    """Schema for updating an article."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=10)
    summary: Optional[str] = None
    ticker_symbols: Optional[str] = Field(None, max_length=500)
    market_sector: Optional[str] = Field(None, max_length=100)
    is_processed: Optional[bool] = None


class Article(ArticleBase):
    """Schema for Article responses."""
    id: int
    scraped_at: datetime
    updated_at: Optional[datetime]
    is_processed: bool = False
    processing_error: Optional[str] = None
    word_count: Optional[int] = None
    reading_time_minutes: Optional[float] = None
    
    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy compatibility


# Reddit Post schemas
class RedditPostBase(BaseModel):
    """Base schema for Reddit posts."""
    reddit_id: str = Field(..., min_length=1, max_length=50, description="Reddit post ID")
    reddit_url: str = Field(..., description="Reddit post URL")
    title: str = Field(..., min_length=1, max_length=300, description="Post title")
    subreddit: str = Field(..., min_length=1, max_length=50, description="Subreddit name")
    author: Optional[str] = Field(None, max_length=100, description="Reddit username")
    content: Optional[str] = Field(None, description="Post content")
    post_type: PostType = Field(..., description="Type of Reddit post")
    score: int = Field(default=0, description="Reddit score (upvotes - downvotes)")
    upvote_ratio: Optional[float] = Field(None, ge=0.0, le=1.0, description="Upvote ratio")
    num_comments: int = Field(default=0, ge=0, description="Number of comments")
    created_at: datetime = Field(..., description="Post creation timestamp")
    ticker_symbols: Optional[str] = Field(None, max_length=500)
    flair: Optional[str] = Field(None, max_length=100, description="Post flair")


class RedditPostCreate(RedditPostBase):
    """Schema for creating a Reddit post."""
    pass


class RedditPost(RedditPostBase):
    """Schema for Reddit post responses."""
    id: int
    scraped_at: datetime
    updated_at: Optional[datetime]
    is_processed: bool = False
    processing_error: Optional[str] = None
    word_count: Optional[int] = None
    contains_positions: bool = False
    mention_count: int = 0
    is_removed: bool = False
    is_locked: bool = False
    is_nsfw: bool = False
    is_spoiler: bool = False
    
    class Config:
        from_attributes = True


# Sentiment Score schemas
class SentimentScoreBase(BaseModel):
    """Base schema for sentiment scores."""
    model_name: str = Field(..., min_length=1, max_length=50, description="Sentiment model name")
    model_version: Optional[str] = Field(None, max_length=20, description="Model version")
    compound_score: float = Field(..., ge=-1.0, le=1.0, description="Compound sentiment score")
    positive_score: float = Field(..., ge=0.0, le=1.0, description="Positive sentiment score")
    negative_score: float = Field(..., ge=0.0, le=1.0, description="Negative sentiment score")
    neutral_score: float = Field(..., ge=0.0, le=1.0, description="Neutral sentiment score")
    sentiment_label: SentimentLabel = Field(..., description="Sentiment classification")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Model confidence")
    financial_sentiment: Optional[float] = Field(None, ge=-1.0, le=1.0, description="Financial-specific sentiment")
    market_direction: Optional[MarketDirection] = Field(None, description="Market direction indicator")
    text_length: int = Field(..., gt=0, description="Length of analyzed text")
    word_count: int = Field(..., gt=0, description="Word count of analyzed text")
    
    @validator('positive_score', 'negative_score', 'neutral_score')
    def validate_score_sum(cls, v, values):
        """Validate that sentiment scores approximately sum to 1.0."""
        if 'positive_score' in values and 'negative_score' in values:
            total = v + values.get('positive_score', 0) + values.get('negative_score', 0)
            if not (0.95 <= total <= 1.05):  # Allow small floating point errors
                raise ValueError('Sentiment scores must sum to approximately 1.0')
        return v


class SentimentScoreCreate(SentimentScoreBase):
    """Schema for creating sentiment scores."""
    article_id: Optional[int] = None
    reddit_post_id: Optional[int] = None
    
    @validator('article_id', 'reddit_post_id')
    def validate_source_reference(cls, v, values):
        """Ensure exactly one source is referenced."""
        article_id = values.get('article_id') if 'article_id' in values else v
        reddit_post_id = values.get('reddit_post_id') if 'reddit_post_id' in values else v
        
        if not (bool(article_id) ^ bool(reddit_post_id)):
            raise ValueError('Exactly one of article_id or reddit_post_id must be provided')
        return v


class SentimentScore(SentimentScoreBase):
    """Schema for sentiment score responses."""
    id: int
    article_id: Optional[int] = None
    reddit_post_id: Optional[int] = None
    analyzed_at: datetime
    sentence_count: Optional[int] = None
    financial_keywords: Optional[str] = None
    ticker_mentions: Optional[str] = None
    processing_time_ms: Optional[float] = None
    has_financial_context: bool = False
    is_spam_detected: bool = False
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        from_attributes = True


# Response models for API endpoints
class PaginationInfo(BaseModel):
    """Pagination information for list responses."""
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, le=100, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of items")
    pages: int = Field(..., ge=0, description="Total number of pages")
    has_prev: bool = Field(..., description="Has previous page")
    has_next: bool = Field(..., description="Has next page")


class ArticleListResponse(BaseModel):
    """Response model for article list endpoints."""
    articles: List[Article]
    pagination: PaginationInfo


class RedditPostListResponse(BaseModel):
    """Response model for Reddit post list endpoints."""
    reddit_posts: List[RedditPost]
    pagination: PaginationInfo


class SentimentScoreListResponse(BaseModel):
    """Response model for sentiment score list endpoints."""
    sentiment_scores: List[SentimentScore]
    pagination: PaginationInfo


# Analytics and aggregation schemas
class SentimentAnalytics(BaseModel):
    """Aggregated sentiment analytics."""
    total_analyzed: int = Field(..., ge=0, description="Total items analyzed")
    positive_count: int = Field(..., ge=0, description="Number of positive sentiments")
    negative_count: int = Field(..., ge=0, description="Number of negative sentiments")
    neutral_count: int = Field(..., ge=0, description="Number of neutral sentiments")
    average_sentiment: float = Field(..., ge=-1.0, le=1.0, description="Average sentiment score")
    sentiment_trend: str = Field(..., description="Overall sentiment trend")
    
    @validator('sentiment_trend')
    def validate_trend(cls, v):
        """Validate sentiment trend values."""
        allowed_trends = ['improving', 'declining', 'stable', 'volatile']
        if v not in allowed_trends:
            raise ValueError(f'Trend must be one of: {allowed_trends}')
        return v


class TickerSentiment(BaseModel):
    """Sentiment analysis for specific ticker symbols."""
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    total_mentions: int = Field(..., ge=0, description="Total mentions across all sources")
    average_sentiment: float = Field(..., ge=-1.0, le=1.0, description="Average sentiment score")
    sentiment_label: SentimentLabel = Field(..., description="Overall sentiment classification")
    article_mentions: int = Field(..., ge=0, description="Mentions in news articles")
    reddit_mentions: int = Field(..., ge=0, description="Mentions in Reddit posts")
    last_updated: datetime = Field(..., description="Last update timestamp")


class MarketSentimentSummary(BaseModel):
    """Summary of market sentiment across all sources."""
    overall_sentiment: float = Field(..., ge=-1.0, le=1.0, description="Overall market sentiment")
    sentiment_label: SentimentLabel = Field(..., description="Overall sentiment classification")
    total_sources: int = Field(..., ge=0, description="Total number of sources analyzed")
    trending_tickers: List[TickerSentiment] = Field(..., max_items=20, description="Top trending stocks")
    sentiment_by_source: dict = Field(..., description="Sentiment breakdown by source")
    analysis_timestamp: datetime = Field(..., description="Analysis timestamp")


# Error response schemas
class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")