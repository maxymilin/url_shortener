def test_root(test_app):
    """Test the main page."""
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}


def test_get_url_coutn_empty(test_app):
    """Test the count of shortener url,
    when no urls have been shortened yet."""
    response = test_app.get("/count")
    assert response.status_code == 200
    assert response.json() == {"message": "Number of shortened urls: 0"}


def test_get_top_10_empty(test_app):
    """Test the top 10 of shortener url,
    when no urls have been shortened yet."""
    response = test_app.get("/top10")
    assert response.status_code == 200
    assert response.json() == {"top_10_url": []}
