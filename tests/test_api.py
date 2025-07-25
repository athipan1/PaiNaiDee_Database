from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api.main import app
from api.deps import get_db

# Create a mock database session
mock_db = MagicMock()

# Override the database dependency
app.dependency_overrides[get_db] = lambda: mock_db

client = TestClient(app)


def test_root():
    # Mock the crud function to return empty list
    with client:
        r = client.get("/attractions")
        assert r.status_code == 200