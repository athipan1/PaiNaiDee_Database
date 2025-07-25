import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import tempfile
import os

from api.main import app
from api.models import Base
from api.deps import get_db
from api import schemas

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "user"
    }

@pytest.fixture
def test_admin_data():
    """Test admin user data."""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword123",
        "role": "admin"
    }

@pytest.fixture
def test_category_data():
    """Test category data."""
    return {
        "name": "Test Category",
        "description": "Test category description",
        "icon_url": "https://example.com/icon.png"
    }

@pytest.fixture
def test_tag_data():
    """Test tag data."""
    return {
        "name": "Test Tag"
    }

@pytest.fixture
def test_attraction_data():
    """Test attraction data."""
    return {
        "name": "Test Attraction",
        "description": "Test attraction description",
        "address": "123 Test Street",
        "province": "Test Province",
        "district": "Test District",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "category_id": 1,
        "opening_hours": "9:00-17:00",
        "entrance_fee": "100 บาท",
        "contact_phone": "+66-2-1234567",
        "website": "https://test-attraction.com",
        "main_image_url": "https://example.com/image.jpg",
        "tag_ids": []
    }

class TestHealthCheck:
    """Test health check endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to PaiNaiDee API" in response.json()["message"]

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_register_user(self, client, test_user_data, db_session):
        """Test user registration."""
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert data["role"] == test_user_data["role"]
        assert "user_id" in data
    
    def test_register_duplicate_username(self, client, test_user_data, db_session):
        """Test registration with duplicate username."""
        # Register first user
        client.post("/auth/register", json=test_user_data)
        
        # Try to register with same username
        duplicate_data = test_user_data.copy()
        duplicate_data["email"] = "different@example.com"
        
        response = client.post("/auth/register", json=duplicate_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_success(self, client, test_user_data, db_session):
        """Test successful login."""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_user_data, db_session):
        """Test login with invalid credentials."""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 401
    
    def test_get_current_user(self, client, test_user_data, db_session):
        """Test getting current user info."""
        # Register and login
        client.post("/auth/register", json=test_user_data)
        
        login_response = client.post("/auth/token", data={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        })
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get current user info
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]

class TestCategories:
    """Test category endpoints."""
    
    def test_create_category_as_admin(self, client, test_admin_data, test_category_data, db_session):
        """Test creating category as admin."""
        # Register admin and get token
        client.post("/auth/register", json=test_admin_data)
        login_response = client.post("/auth/token", data={
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create category
        response = client.post("/categories", json=test_category_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == test_category_data["name"]
        assert data["description"] == test_category_data["description"]
        assert "category_id" in data
    
    def test_get_categories(self, client, db_session):
        """Test getting all categories."""
        response = client.get("/categories")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_category_as_user_forbidden(self, client, test_user_data, test_category_data, db_session):
        """Test that regular users cannot create categories."""
        # Register user and get token
        client.post("/auth/register", json=test_user_data)
        login_response = client.post("/auth/token", data={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to create category
        response = client.post("/categories", json=test_category_data, headers=headers)
        assert response.status_code == 403

class TestAttractions:
    """Test attraction endpoints."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        Base.metadata.create_all(bind=engine)
    
    def test_get_attractions(self, client, db_session):
        """Test getting all attractions."""
        response = client.get("/attractions")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_attraction_not_found(self, client, db_session):
        """Test getting non-existent attraction."""
        response = client.get("/attractions/99999")
        assert response.status_code == 404
    
    def test_create_attraction_as_admin(self, client, test_admin_data, test_category_data, test_attraction_data, db_session):
        """Test creating attraction as admin."""
        # Register admin and get token
        client.post("/auth/register", json=test_admin_data)
        login_response = client.post("/auth/token", data={
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create category first
        category_response = client.post("/categories", json=test_category_data, headers=headers)
        category_id = category_response.json()["category_id"]
        
        # Update attraction data with valid category_id
        test_attraction_data["category_id"] = category_id
        
        # Create attraction
        response = client.post("/attractions", json=test_attraction_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == test_attraction_data["name"]
        assert data["description"] == test_attraction_data["description"]
        assert "id" in data

class TestReviews:
    """Test review endpoints."""
    
    def test_get_reviews(self, client, db_session):
        """Test getting all reviews."""
        response = client.get("/reviews")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_review_requires_auth(self, client, db_session):
        """Test that creating review requires authentication."""
        review_data = {
            "attraction_id": 1,
            "rating": 5,
            "comment": "Great place!"
        }
        
        response = client.post("/reviews", json=review_data)
        assert response.status_code == 401

class TestFavorites:
    """Test favorite endpoints."""
    
    def test_get_favorites_requires_auth(self, client, db_session):
        """Test that getting favorites requires authentication."""
        response = client.get("/favorites")
        assert response.status_code == 401
    
    def test_create_favorite_requires_auth(self, client, db_session):
        """Test that creating favorite requires authentication."""
        favorite_data = {"attraction_id": 1}
        
        response = client.post("/favorites", json=favorite_data)
        assert response.status_code == 401

class TestRecommendations:
    """Test recommendation endpoints."""
    
    def test_get_recommendations_requires_auth(self, client, db_session):
        """Test that getting recommendations requires authentication."""
        response = client.get("/recommendations")
        assert response.status_code == 401
    
    def test_get_trending_attractions(self, client, db_session):
        """Test getting trending attractions (public endpoint)."""
        response = client.get("/recommendations/trending")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_location_recommendations(self, client, db_session):
        """Test getting location-based recommendations."""
        response = client.get("/recommendations/location/กรุงเทพมหานคร")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestSearch:
    """Test search functionality."""
    
    def test_search_attractions(self, client, db_session):
        """Test searching attractions."""
        search_data = {
            "keyword": "test",
            "province": "กรุงเทพมหานคร",
            "skip": 0,
            "limit": 10
        }
        
        response = client.post("/attractions/search", json=search_data)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_attractions_with_filters(self, client, db_session):
        """Test searching attractions with various filters."""
        search_data = {
            "keyword": "temple",
            "province": "กรุงเทพมหานคร",
            "min_rating": 4.0,
            "max_rating": 5.0,
            "skip": 0,
            "limit": 5
        }
        
        response = client.post("/attractions/search", json=search_data)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestDataValidation:
    """Test data validation."""
    
    def test_invalid_email_format(self, client, db_session):
        """Test registration with invalid email format."""
        invalid_user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123"
        }
        
        response = client.post("/auth/register", json=invalid_user_data)
        assert response.status_code == 422  # Validation error
    
    def test_short_password(self, client, db_session):
        """Test registration with short password."""
        invalid_user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"  # Too short
        }
        
        response = client.post("/auth/register", json=invalid_user_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_rating_range(self, client, test_user_data, db_session):
        """Test creating review with invalid rating."""
        # Register user and get token
        client.post("/auth/register", json=test_user_data)
        login_response = client.post("/auth/token", data={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to create review with invalid rating
        review_data = {
            "attraction_id": 1,
            "rating": 6,  # Invalid rating (should be 1-5)
            "comment": "Test review"
        }
        
        response = client.post("/reviews", json=review_data, headers=headers)
        assert response.status_code == 422  # Validation error

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])