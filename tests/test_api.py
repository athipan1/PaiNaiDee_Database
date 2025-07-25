from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api.main import app
from api.deps import get_db


# Mock the database dependency
def mock_get_db():
    return MagicMock()


app.dependency_overrides[get_db] = mock_get_db
client = TestClient(app)


def test_root():
    r = client.get("/attractions")
    assert r.status_code == 200
