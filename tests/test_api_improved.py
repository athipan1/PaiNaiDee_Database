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


def test_health_check(test_client):
    """Test basic application health"""
    response = test_client.get("/docs")
    assert response.status_code == 200
