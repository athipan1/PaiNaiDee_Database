from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Use SQLite for testing if in test environment, otherwise PostgreSQL
if os.getenv("TESTING") == "true":
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Got0896177698@localhost:5432/painaidee_db")
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()