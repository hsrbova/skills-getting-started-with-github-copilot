import pytest
from src.app import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_get_activities(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    email = "tester@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup?email={email}"

    # Act
    first_response = client.post(endpoint)
    duplicate_response = client.post(endpoint)

    # Assert
    assert first_response.status_code == 200
    assert "Signed up tester@mergington.edu" in first_response.json()["message"]
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up"


def test_signup_activity_not_found(client):
    # Arrange
    endpoint = "/activities/Nonexistent/signup?email=ghost@mergington.edu"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister(client):
    # Arrange
    activity_name = "Programming Class"
    email = "remove@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup?email={email}"
    client.post(endpoint)

    # Act
    delete_response = client.delete(endpoint)
    delete_again_response = client.delete(endpoint)

    # Assert
    assert delete_response.status_code == 200
    assert "Removed remove@mergington.edu" in delete_response.json()["message"]
    assert delete_again_response.status_code == 404
    assert delete_again_response.json()["detail"] == "Student not signed up"


def test_unregister_activity_not_found(client):
    # Arrange
    endpoint = "/activities/Nonexistent/signup?email=ghost@mergington.edu"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
