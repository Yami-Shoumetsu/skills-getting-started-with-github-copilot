from urllib.parse import quote


def test_get_activities_returns_structure(client):
    # Arrange: client fixture provided

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "alice@example.com"
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_raises_400(client):
    # Arrange
    activity = "Chess Club"
    email = "bob@example.com"

    # First signup should succeed
    resp1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp1.status_code == 200

    # Act: duplicate signup
    resp2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp2.status_code == 400


def test_remove_participant_success(client):
    # Arrange
    activity = "Tennis Club"
    email = "newplayer@example.com"

    # Ensure participant is present by signing up first
    signup = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert signup.status_code == 200

    # Act: remove participant
    response = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_participant_404(client):
    # Arrange
    activity = "Programming Class"
    email = "doesnotexist@example.com"

    # Act
    response = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_signup_activity_not_found_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "x@example.com"

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
