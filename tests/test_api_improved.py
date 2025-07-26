import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app
from api.deps import get_db
from api.models import Base

# Test database configuration
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/painaidee_test_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="session")
def setup_database():
    """Set up test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client(setup_database):
    """Create test client"""
    return client


def test_root(test_client):
    """Test the root attractions endpoint"""
    response = test_client.get("/attractions")
    assert response.status_code == 200
    # Should return empty list if no attractions exist
    assert isinstance(response.json(), list)


def test_attraction_not_found(test_client):
    """Test attraction endpoint with non-existent ID"""
    response = test_client.get("/attractions/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_recommend_endpoint(test_client):
    """Test recommendation endpoint"""
    # This should handle missing user gracefully
    response = test_client.get("/recommend?user_id=1")
    # The endpoint should at least respond (might be empty list or error)
    assert response.status_code in [200, 404, 422]


def test_health_check():
    """Test basic application health"""
    response = client.get("/docs")
    assert response.status_code == 200
