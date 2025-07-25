from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from api.main import app
from api.deps import get_db


# Mock database dependency
def override_get_db():
    mock_db = MagicMock()
    try:
        yield mock_db
    finally:
        pass


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    # Mock the crud.get_attractions function to return an empty list
    with patch('api.main.crud.get_attractions', return_value=[]):
        r = client.get("/attractions")
        assert r.status_code == 200
