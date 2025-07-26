import os
import pytest
from fastapi.testclient import TestClient

# Set testing environment variable
os.environ["TESTING"] = "true"

from api.main import app
from api.models import Base
from api.deps import engine

# Create tables for testing
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_root():
    """Test that the attractions endpoint returns 200"""
    r = client.get("/attractions")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_single_attraction_not_found():
    """Test that getting a non-existent attraction returns 404"""
    r = client.get("/attractions/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"