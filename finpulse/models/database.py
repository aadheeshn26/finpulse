"""
Database connection and session management.

This module sets up the SQLAlchemy database connection, session factory,
and base model class for all database models.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Database URL - using SQLite for simplicity, but can easily switch to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finpulse.db")

# Create SQLAlchemy engine
# For SQLite, we need to configure it to work with FastAPI's threading
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Disabled for cleaner Power BI integration
    )
else:
    # For PostgreSQL or other databases
    engine = create_engine(DATABASE_URL, echo=False)

# Create SessionLocal class - each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class - all our models will inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    This will be used with FastAPI's dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.
    This function should be called when starting the application.
    """
    Base.metadata.create_all(bind=engine)