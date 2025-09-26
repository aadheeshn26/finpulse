#!/usr/bin/env python3
"""
FinPulse FastAPI Application

Main application entry point providing REST API endpoints
for financial sentiment analysis data.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from finpulse.models.database import get_db, create_tables
from finpulse.models import Article, RedditPost, SentimentScore
from finpulse.api.schemas import (
    Article as ArticleSchema,
    RedditPost as RedditPostSchema,
    SentimentScore as SentimentScoreSchema,
    ArticleListResponse,
    PaginationInfo,
    MarketSentimentSummary,
    SentimentLabel
)
from config.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    create_tables()
    print("🚀 FinPulse API started successfully!")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to FinPulse - Financial Sentiment Analysis API",
        "version": settings.api_version,
        "endpoints": {
            "articles": "/articles",
            "reddit_posts": "/reddit-posts", 
            "sentiment": "/sentiment",
            "analytics": "/analytics",
            "docs": "/docs"
        }
    }


@app.get("/articles", response_model=ArticleListResponse)
async def get_articles(
    skip: int = Query(0, ge=0, description="Number of articles to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of articles to return"),
    source: Optional[str] = Query(None, description="Filter by news source"),
    db: Session = Depends(get_db)
):
    """Get paginated list of articles."""
    query = db.query(Article)
    
    if source:
        query = query.filter(Article.source == source)
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    
    return ArticleListResponse(
        articles=[ArticleSchema.from_orm(article) for article in articles],
        pagination=PaginationInfo(
            page=(skip // limit) + 1,
            per_page=limit,
            total=total,
            pages=(total + limit - 1) // limit,
            has_prev=skip > 0,
            has_next=skip + limit < total
        )
    )


@app.get("/sentiment/summary")
async def get_sentiment_summary(db: Session = Depends(get_db)):
    """Get overall sentiment analysis summary."""
    
    # Get basic sentiment counts
    total_scores = db.query(SentimentScore).count()
    positive_count = db.query(SentimentScore).filter(
        SentimentScore.sentiment_label == SentimentLabel.POSITIVE
    ).count()
    negative_count = db.query(SentimentScore).filter(
        SentimentScore.sentiment_label == SentimentLabel.NEGATIVE
    ).count()
    neutral_count = db.query(SentimentScore).filter(
        SentimentScore.sentiment_label == SentimentLabel.NEUTRAL
    ).count()
    
    # Calculate average sentiment
    avg_sentiment = db.query(SentimentScore).with_entities(
        db.func.avg(SentimentScore.compound_score).label('avg_sentiment')
    ).scalar() or 0.0
    
    return {
        "total_analyzed": total_scores,
        "sentiment_distribution": {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        },
        "average_sentiment": round(float(avg_sentiment), 3),
        "overall_trend": "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "FinPulse API"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )