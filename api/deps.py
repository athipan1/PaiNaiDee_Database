from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Use environment variable with fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Handle different database URLs gracefully
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Warning: Database connection failed: {e}")
    # Fallback to SQLite for testing
    engine = create_engine("sqlite:///./test.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Database session error: {e}")
        yield None
    finally:
        try:
            db.close()
        except Exception:
            pass
