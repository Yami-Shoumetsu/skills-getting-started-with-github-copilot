def test_root_redirects_to_static_index(client):
    # Arrange: client fixture

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers.get("location", "").endswith("/static/index.html")


def test_static_index_served(client):
    # Arrange

    # Act
    response = client.get("/static/index.html")

    # Assert
    assert response.status_code == 200
    assert "<html" in response.text.lower()
