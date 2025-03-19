"""
Database configuration module for the Common Assessment Tool.
Handles database connection and session management using SQLAlchemy.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load database URL from environment variable (default to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configure session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Creates and yields a database session, ensuring it is closed properly.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()