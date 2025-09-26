#!/usr/bin/env python3
"""
Sample data generator for FinPulse demo.

Creates realistic sample data for articles, Reddit posts, and sentiment scores
to demonstrate the Power BI dashboard functionality.
"""

import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from finpulse.models.database import SessionLocal, create_tables
from finpulse.models import Article, RedditPost, SentimentScore
from finpulse.sentiment import SentimentAnalyzer

# Sample data for realistic articles
SAMPLE_ARTICLES = [
    {
        "title": "Apple Reports Strong Q4 Earnings Despite Market Volatility",
        "content": "Apple Inc. exceeded analyst expectations with robust quarterly earnings, driven by strong iPhone sales and services revenue growth. The company's resilient performance demonstrates its ability to navigate challenging market conditions.",
        "source": "Yahoo Finance",
        "author": "Tech Reporter",
        "ticker_symbols": "AAPL",
        "market_sector": "Technology"
    },
    {
        "title": "Tesla Stock Surges on Autopilot Technology Breakthrough",
        "content": "Tesla shares jumped 8% in after-hours trading following the announcement of significant improvements to its Full Self-Driving capabilities. The breakthrough could accelerate the company's autonomous vehicle timeline.",
        "source": "Reuters",
        "author": "Auto Industry Analyst",
        "ticker_symbols": "TSLA",
        "market_sector": "Automotive"
    },
    {
        "title": "Microsoft Azure Cloud Revenue Beats Expectations",
        "content": "Microsoft's cloud computing division Azure reported 25% year-over-year growth, significantly outpacing competitor offerings. The strong performance solidifies Microsoft's position in the enterprise cloud market.",
        "source": "Bloomberg",
        "author": "Cloud Computing Specialist",
        "ticker_symbols": "MSFT",
        "market_sector": "Technology"
    },
    {
        "title": "Amazon Faces Regulatory Scrutiny Over Market Dominance",
        "content": "Federal regulators are investigating Amazon's business practices, particularly its treatment of third-party sellers and competitive positioning. The probe could result in significant operational changes for the e-commerce giant.",
        "source": "Wall Street Journal",
        "author": "Regulatory Reporter",
        "ticker_symbols": "AMZN",
        "market_sector": "E-commerce"
    },
    {
        "title": "Google Parent Alphabet Invests Heavily in AI Research",
        "content": "Alphabet announced a $2 billion investment in artificial intelligence research and development, aiming to maintain its competitive edge in the rapidly evolving AI landscape. The investment spans multiple AI applications including search, cloud, and autonomous systems.",
        "source": "TechCrunch",
        "author": "AI Industry Expert",
        "ticker_symbols": "GOOGL",
        "market_sector": "Technology"
    }
]

SAMPLE_REDDIT_POSTS = [
    {
        "title": "AAPL to the moon! 🚀 Strong earnings beat expectations",
        "content": "Just saw Apple's earnings report and I'm bullish AF! Revenue up, services growing, iPhone sales strong. This is going to $200 easy. Already loaded up on calls!",
        "subreddit": "wallstreetbets",
        "author": "DiamondHands123",
        "reddit_id": "abc123",
        "post_type": "text",
        "score": 1543,
        "ticker_symbols": "AAPL",
        "flair": "YOLO"
    },
    {
        "title": "Tesla FSD update is actually impressive - hold or sell?",
        "content": "Been testing the new FSD beta and it's genuinely good. Way better than previous versions. Thinking this might be the catalyst TSLA needs. What's everyone's thoughts?",
        "subreddit": "investing",
        "author": "TechInvestor2024",
        "reddit_id": "def456", 
        "post_type": "text",
        "score": 487,
        "ticker_symbols": "TSLA",
        "flair": "Discussion"
    },
    {
        "title": "Microsoft is quietly dominating the cloud space",
        "content": "Azure growth is insane. Enterprise customers are choosing MSFT over AWS more and more. This stock is undervalued compared to other tech giants IMO.",
        "subreddit": "stocks",
        "author": "CloudWatcher",
        "reddit_id": "ghi789",
        "post_type": "text", 
        "score": 234,
        "ticker_symbols": "MSFT",
        "flair": "Analysis"
    }
]


def generate_sample_data():
    """Generate sample data for demonstration."""
    print("🔄 Generating sample data for FinPulse...")
    
    # Create tables if they don't exist
    create_tables()
    
    # Initialize sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(SentimentScore).delete()
        db.query(Article).delete() 
        db.query(RedditPost).delete()
        db.commit()
        print("🗑️  Cleared existing data")
        
        # Generate articles
        print("📰 Creating sample articles...")
        for i, article_data in enumerate(SAMPLE_ARTICLES):
            # Create article with varied dates
            article = Article(
                title=article_data["title"],
                url=f"https://example.com/article-{i+1}",
                source=article_data["source"],
                author=article_data["author"],
                content=article_data["content"],
                published_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                ticker_symbols=article_data["ticker_symbols"],
                market_sector=article_data["market_sector"],
                word_count=len(article_data["content"].split()),
                reading_time_minutes=len(article_data["content"].split()) / 200,
                is_processed=True
            )
            
            db.add(article)
            db.commit()
            db.refresh(article)
            
            # Generate sentiment analysis
            sentiment_result = analyzer.analyze_text(article_data["content"])
            
            sentiment_score = SentimentScore(
                article_id=article.id,
                model_name=sentiment_result["model_name"],
                compound_score=sentiment_result["compound_score"],
                positive_score=sentiment_result["positive_score"],
                negative_score=sentiment_result["negative_score"],
                neutral_score=sentiment_result["neutral_score"],
                sentiment_label=sentiment_result["sentiment_label"],
                confidence=sentiment_result["confidence"],
                text_length=sentiment_result["text_length"],
                word_count=sentiment_result["word_count"],
                processing_time_ms=sentiment_result["processing_time_ms"],
                has_financial_context=True,
                ticker_mentions=article_data["ticker_symbols"]
            )
            
            db.add(sentiment_score)
            print(f"  ✅ Created article: {article.title[:50]}...")
        
        # Generate Reddit posts
        print("💬 Creating sample Reddit posts...")
        for post_data in SAMPLE_REDDIT_POSTS:
            reddit_post = RedditPost(
                reddit_id=post_data["reddit_id"],
                reddit_url=f"https://reddit.com/r/{post_data['subreddit']}/comments/{post_data['reddit_id']}",
                title=post_data["title"],
                subreddit=post_data["subreddit"],
                author=post_data["author"],
                content=post_data["content"],
                post_type=post_data["post_type"],
                score=post_data["score"],
                upvote_ratio=random.uniform(0.7, 0.95),
                num_comments=random.randint(50, 500),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 7)),
                ticker_symbols=post_data["ticker_symbols"],
                flair=post_data["flair"],
                word_count=len(post_data["content"].split()) if post_data["content"] else 0,
                mention_count=1,
                contains_positions=True,
                is_processed=True
            )
            
            db.add(reddit_post)
            db.commit()
            db.refresh(reddit_post)
            
            # Generate sentiment analysis
            sentiment_result = analyzer.analyze_text(post_data["content"])
            
            sentiment_score = SentimentScore(
                reddit_post_id=reddit_post.id,
                model_name=sentiment_result["model_name"], 
                compound_score=sentiment_result["compound_score"],
                positive_score=sentiment_result["positive_score"],
                negative_score=sentiment_result["negative_score"],
                neutral_score=sentiment_result["neutral_score"],
                sentiment_label=sentiment_result["sentiment_label"],
                confidence=sentiment_result["confidence"],
                text_length=sentiment_result["text_length"],
                word_count=sentiment_result["word_count"],
                processing_time_ms=sentiment_result["processing_time_ms"],
                has_financial_context=True,
                ticker_mentions=post_data["ticker_symbols"]
            )
            
            db.add(sentiment_score)
            print(f"  ✅ Created Reddit post: {reddit_post.title[:50]}...")
            
        db.commit()
        
        # Print summary
        article_count = db.query(Article).count()
        reddit_count = db.query(RedditPost).count()
        sentiment_count = db.query(SentimentScore).count()
        
        print(f"\n🎉 Sample data generated successfully!")
        print(f"📊 Summary:")
        print(f"   - Articles: {article_count}")
        print(f"   - Reddit Posts: {reddit_count}")
        print(f"   - Sentiment Scores: {sentiment_count}")
        print(f"\n🚀 Ready for Power BI integration!")
        
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        db.rollback()
        
    finally:
        db.close()


if __name__ == "__main__":
    generate_sample_data()