#!/usr/bin/env python3
"""
Database initialization script for PaiNaiDee
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base

def init_database():
    """Initialize the database with tables"""
    # Get database URL from environment variables
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "painaidee_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_port = os.getenv("DB_PORT", "5432")
    
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    print(f"Connecting to database: {db_host}:{db_port}/{db_name}")
    
    # Create engine and tables
    engine = create_engine(database_url)
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization completed successfully!")

if __name__ == "__main__":
    init_database()