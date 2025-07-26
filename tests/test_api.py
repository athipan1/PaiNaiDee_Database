import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set testing environment variable
os.environ["TESTING"] = "true"

from api.main import app
from api.models import Base, User, Category, Attraction
from api.deps import get_db

# Create a test database
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for testing
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def setup_test_data():
    """Setup test data in the database"""
    db = TestingSessionLocal()
    try:
        # Clear existing data
        db.query(Attraction).delete()
        db.query(Category).delete()
        db.query(User).delete()
        
        # Create test category
        category = Category(
            name="สถานที่ท่องเที่ยว",
            description="หมวดหมู่สำหรับสถานที่ท่องเที่ยว",
            icon_url="https://example.com/icon.png"
        )
        db.add(category)
        db.flush()
        
        # Create test user
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role="user"
        )
        db.add(user)
        db.flush()
        
        # Create test attraction
        attraction = Attraction(
            name="วัดพระแก้ว",
            description="วัดสวยงามในกรุงเทพฯ",
            address="ถนนนาพระลาน เขตพระนคร",
            province="กรุงเทพมหานคร",
            district="พระนคร",
            latitude=13.7516,
            longitude=100.4921,
            category_id=category.category_id,
            opening_hours="08:30-16:30",
            entrance_fee="500 บาท",
            website="https://www.watphrakaew.com"
        )
        db.add(attraction)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def test_root():
    """Test that the attractions endpoint returns 200"""
    r = client.get("/attractions")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_single_attraction_not_found():
    """Test that getting a non-existent attraction returns 404"""
    r = client.get("/attractions/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "ไม่พบสถานที่ท่องเที่ยว"

def test_get_attractions_with_data(setup_test_data):
    """Test getting attractions when data exists"""
    r = client.get("/attractions")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "วัดพระแก้ว"
    assert data[0]["province"] == "กรุงเทพมหานคร"

def test_get_single_attraction_with_data(setup_test_data):
    """Test getting a specific attraction"""
    # First get all attractions to find an ID
    r = client.get("/attractions")
    attractions = r.json()
    assert len(attractions) > 0
    
    attraction_id = attractions[0]["id"]
    
    # Now get the specific attraction
    r = client.get(f"/attractions/{attraction_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "วัดพระแก้ว"
    assert data["province"] == "กรุงเทพมหานคร"

def test_get_recommendations(setup_test_data):
    """Test the recommendation endpoint"""
    r = client.get("/recommend?user_id=1")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # Should return attractions since user has no reviews yet

def test_health_check():
    """Test the health check endpoint"""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_root_endpoint():
    """Test the root endpoint"""
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    assert "documentation" in data