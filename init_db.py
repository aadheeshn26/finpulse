#!/usr/bin/env python3
"""
Database initialization script for FinPulse.

This script creates all database tables and can be used to reset
the database during development.
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from finpulse.models.database import create_tables, engine, Base
from finpulse.models import Article, RedditPost, SentimentScore
from sqlalchemy import inspect


def main():
    """Initialize the database tables."""
    print("🚀 Initializing FinPulse Database...")
    
    try:
        # Create all tables
        print("📊 Creating database tables...")
        create_tables()
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Successfully created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        print("\n🎉 Database initialization completed successfully!")
        print(f"📍 Database location: {engine.url}")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()