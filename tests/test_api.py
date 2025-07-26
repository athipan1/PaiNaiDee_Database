def test_root(test_client):
    """Test the root attractions endpoint"""
    response = test_client.get("/attractions")
    assert response.status_code == 200
    # Should return empty list if no attractions exist
    assert isinstance(response.json(), list)
