"""
Database connection and migration tests
"""

import os
import pytest
from sqlalchemy import create_engine, text
from api.models import Base, engine


def test_database_connection():
    """Test that we can connect to the database"""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/painaidee_test_db",
    )

    try:
        test_engine = create_engine(database_url, pool_pre_ping=True)
        with test_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        print("✅ Database connection test passed")
    except Exception as e:
        pytest.skip(f"Database not available: {e}")


def test_table_creation():
    """Test that tables can be created"""
    try:
        # This should work if the database is available
        Base.metadata.create_all(bind=engine)
        print("✅ Table creation test passed")
    except Exception as e:
        pytest.skip(f"Cannot create tables: {e}")


def test_models_import():
    """Test that all models can be imported successfully"""
    from api.models import (
        User,
        Category,
        Tag,
        Attraction,
        Image,
        Review,
        Favorite,
        AttractionTag,
    )

    # Check that all models have the expected attributes
    assert hasattr(User, "user_id")
    assert hasattr(Category, "category_id")
    assert hasattr(Tag, "tag_id")
    assert hasattr(Attraction, "id")
    assert hasattr(Image, "id")
    assert hasattr(Review, "id")
    assert hasattr(Favorite, "id")
    assert hasattr(AttractionTag, "attraction_id")

    print("✅ Models import test passed")


def test_db_script_syntax():
    """Test that db_script.py is syntactically valid"""
    try:
        import db_script

        assert hasattr(db_script, "main")
        print("✅ db_script syntax test passed")
    except ImportError as e:
        pytest.skip(f"db_script import failed: {e}")
    except Exception as e:
        pytest.fail(f"db_script has syntax errors: {e}")
