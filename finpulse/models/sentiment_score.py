"""
Sentiment score model for storing NLP analysis results.

This model stores the sentiment analysis results for both articles
and Reddit posts using various NLP models and techniques.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class SentimentScore(Base):
    """
    Represents sentiment analysis results for articles and Reddit posts.
    
    This model stores the output from various sentiment analysis models
    including VADER, TextBlob, and potentially transformer-based models.
    """
    
    __tablename__ = "sentiment_scores"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key relationships
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True, index=True)
    reddit_post_id = Column(Integer, ForeignKey("reddit_posts.id"), nullable=True, index=True)
    
    # Analysis metadata
    model_name = Column(String(50), nullable=False, index=True)  # "vader", "textblob", "transformer"
    model_version = Column(String(20), nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Sentiment scores - normalized to [-1, 1] range
    compound_score = Column(Float, nullable=False, index=True)  # Overall sentiment (-1 to 1)
    positive_score = Column(Float, nullable=False)  # Positive sentiment probability (0 to 1)
    negative_score = Column(Float, nullable=False)  # Negative sentiment probability (0 to 1)  
    neutral_score = Column(Float, nullable=False)   # Neutral sentiment probability (0 to 1)
    
    # Classification
    sentiment_label = Column(String(20), nullable=False, index=True)  # "positive", "negative", "neutral"
    confidence = Column(Float, nullable=True)  # Model confidence in prediction (0 to 1)
    
    # Context-specific scores
    financial_sentiment = Column(Float, nullable=True)  # Finance-specific sentiment if available
    market_direction = Column(String(20), nullable=True)  # "bullish", "bearish", "neutral"
    
    # Text analysis metadata
    text_length = Column(Integer, nullable=False)  # Character count of analyzed text
    word_count = Column(Integer, nullable=False)   # Word count of analyzed text
    sentence_count = Column(Integer, nullable=True)  # Number of sentences
    
    # Financial keywords detected
    financial_keywords = Column(Text, nullable=True)  # JSON string of detected keywords
    ticker_mentions = Column(String(500), nullable=True)  # Detected ticker symbols
    
    # Processing details
    processing_time_ms = Column(Float, nullable=True)  # Time taken for analysis
    preprocessing_applied = Column(Text, nullable=True)  # Description of preprocessing steps
    
    # Quality indicators
    has_financial_context = Column(Boolean, default=False, nullable=False)
    is_spam_detected = Column(Boolean, default=False, nullable=False)
    quality_score = Column(Float, nullable=True)  # Overall quality assessment (0 to 1)
    
    # Relationships
    article = relationship("Article", back_populates="sentiment_scores")
    reddit_post = relationship("RedditPost", back_populates="sentiment_scores")
    
    def __repr__(self):
        source_type = "Article" if self.article_id else "Reddit"
        source_id = self.article_id or self.reddit_post_id
        return f"<SentimentScore(id={self.id}, {source_type}={source_id}, sentiment='{self.sentiment_label}', score={self.compound_score:.3f})>"
    
    def __str__(self):
        return f"{self.sentiment_label.capitalize()} ({self.compound_score:.3f}) - {self.model_name}"
    
    @property
    def is_positive(self):
        """Returns True if sentiment is positive."""
        return self.sentiment_label == "positive"
    
    @property
    def is_negative(self):
        """Returns True if sentiment is negative."""
        return self.sentiment_label == "negative"
    
    @property
    def is_neutral(self):
        """Returns True if sentiment is neutral."""
        return self.sentiment_label == "neutral"
    
    @property
    def sentiment_strength(self):
        """Returns the absolute strength of sentiment (0 to 1)."""
        return abs(self.compound_score)