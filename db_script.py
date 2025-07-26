"""
Database population script for PaiNaiDee Database

This script fetches data from external APIs and populates the database
with test data for development and testing purposes.
"""

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import random
import datetime
import hashlib
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(__file__))

# Import models from api package instead of duplicating them
try:
    from api.models import (
        Base,
        User,
        Category,
        Tag,
        Attraction,
        Image,
        Review,
        Favorite,
        AttractionTag,
    )

    print("✅ Successfully imported models from api package")
except ImportError as e:
    print(f"❌ Failed to import models: {e}")
    sys.exit(1)

# Database configuration using environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/painaidee_db"
)

# Create database engine and session
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Database connection configured successfully")
except Exception as e:
    print(f"❌ Database connection configuration failed: {e}")
    sys.exit(1)


def check_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Database connection test successful")
        return True
    except Exception as e:
        print(f"⚠️  Database connection test failed: {e}")
        return False


def create_tables():
    """Create database tables if they don't exist"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


def fetch_data_from_api(api_url):
    """
    Fetch JSON data from specified API URL

    Args:
        api_url (str): API URL to fetch data from

    Returns:
        list: List of JSON data from API or empty list if error occurs
    """
    try:
        print(f"Fetching data from: {api_url}")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Successfully fetched {len(data)} items from: {api_url}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error fetching data from API ({api_url}): {e}")
        return []


def save_users_to_db(users_data):
    """Save user data to User table"""
    session = SessionLocal()
    saved_count = 0
    skipped_count = 0
    user_ids = []

    try:
        for user_item in users_data:
            username = user_item.get("username")
            email = user_item.get("email")
            if not username or not email:
                print(f"Skipping user due to missing username or email: {user_item}")
                skipped_count += 1
                continue

            existing_user = (
                session.query(User)
                .filter((User.username == username) | (User.email == email))
                .first()
            )
            if existing_user:
                print(f"Skipping existing user '{username}' or '{email}'")
                skipped_count += 1
                user_ids.append(existing_user.user_id)
                continue

            # Create mock password and hash
            mock_password = f"password_{username}"
            password_hash = hashlib.sha256(mock_password.encode()).hexdigest()

            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                avatar_url=f"https://i.pravatar.cc/150?u={username}",
                role="user",
            )
            session.add(user)
            session.flush()
            user_ids.append(user.user_id)
            saved_count += 1

        session.commit()
        print(
            f"✅ Users saved successfully! Saved: {saved_count}, Skipped: {skipped_count}"
        )
    except Exception as e:
        session.rollback()
        print(f"❌ Error saving users: {e}")
    finally:
        session.close()
    return user_ids


def save_categories_and_tags_to_db(categories_list, tags_list):
    """Save category and tag data to Category and Tag tables"""
    session = SessionLocal()
    saved_categories_count = 0
    saved_tags_count = 0
    category_ids = {}
    tag_ids = {}

    try:
        # Save Categories
        for cat_name in categories_list:
            existing_cat = session.query(Category).filter_by(name=cat_name).first()
            if not existing_cat:
                category = Category(
                    name=cat_name,
                    description=f"Category for {cat_name}",
                    icon_url=f"https://example.com/icons/{cat_name.lower().replace(' ', '_')}.png",
                )
                session.add(category)
                session.flush()
                category_ids[cat_name] = category.category_id
                saved_categories_count += 1
            else:
                category_ids[cat_name] = existing_cat.category_id

        # Save Tags
        for tag_name in tags_list:
            existing_tag = session.query(Tag).filter_by(name=tag_name).first()
            if not existing_tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                session.flush()
                tag_ids[tag_name] = tag.tag_id
                saved_tags_count += 1
            else:
                tag_ids[tag_name] = existing_tag.tag_id

        session.commit()
        print(f"✅ Categories saved: {saved_categories_count}")
        print(f"✅ Tags saved: {saved_tags_count}")
    except Exception as e:
        session.rollback()
        print(f"❌ Error saving categories/tags: {e}")
    finally:
        session.close()
    return category_ids, tag_ids


def get_sample_data_count():
    """Get count of existing data in database"""
    session = SessionLocal()
    try:
        user_count = session.query(User).count()
        category_count = session.query(Category).count()
        attraction_count = session.query(Attraction).count()
        print(f"📊 Current database counts:")
        print(f"  - Users: {user_count}")
        print(f"  - Categories: {category_count}")
        print(f"  - Attractions: {attraction_count}")
        return user_count, category_count, attraction_count
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        return 0, 0, 0
    finally:
        session.close()


def main():
    """Main execution function"""
    print("🚀 Starting PaiNaiDee Database Population Script...")
    print(f"📊 Database URL: {DATABASE_URL}")

    # Test database connection
    if not check_database_connection():
        print("❌ Cannot connect to database. Exiting.")
        return False

    # Create tables
    if not create_tables():
        print("❌ Cannot create database tables. Exiting.")
        return False

    # Get initial data counts
    get_sample_data_count()

    # API endpoints for test data
    API_URL_USERS = "https://jsonplaceholder.typicode.com/users"
    API_URL_POSTS = "https://jsonplaceholder.typicode.com/posts"

    # Predefined categories and tags
    predefined_categories = [
        "Tourist Attraction",
        "Restaurant",
        "Accommodation",
        "Shopping",
        "Nature",
        "History",
        "Culture",
        "Activity",
    ]
    predefined_tags = [
        "Beautiful",
        "Peaceful",
        "Interesting",
        "Delicious",
        "Comfortable",
        "Historical",
        "Cultural",
        "Adventure",
        "Family",
        "Photo Worthy",
        "Hiking",
        "Great View",
    ]

    try:
        # 1. Save categories and tags
        print("\n📝 Saving categories and tags...")
        category_name_to_id, tag_name_to_id = save_categories_and_tags_to_db(
            predefined_categories, predefined_tags
        )

        # 2. Fetch and save users
        print("\n👥 Fetching and saving users...")
        users_data_raw = fetch_data_from_api(API_URL_USERS)
        all_user_ids = save_users_to_db(users_data_raw)

        # Get final data counts
        print("\n📊 Final database state:")
        get_sample_data_count()

        print("\n✅ Database population completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during database population: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
