import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient


# Mock the database dependency before importing the app
def mock_get_db():
    mock_db = MagicMock()
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []
    yield mock_db


# Patch the get_db dependency
with patch('api.deps.get_db', mock_get_db):
    from api.main import app

client = TestClient(app)


def test_root():
    r = client.get("/attractions")
    assert r.status_code == 200
