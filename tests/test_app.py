import pytest
from httpx import AsyncClient
from src.app import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_duplicate(client):
    # Register a new participant
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu" in response.json()["message"]
    # Try duplicate
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_activity_not_found(client):
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister(client):
    # Register, then remove
    client.post("/activities/Programming Class/signup?email=remove@mergington.edu")
    response = client.delete("/activities/Programming Class/signup?email=remove@mergington.edu")
    assert response.status_code == 200
    assert "Removed remove@mergington.edu" in response.json()["message"]
    # Try removing again
    response = client.delete("/activities/Programming Class/signup?email=remove@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up"

def test_unregister_activity_not_found(client):
    response = client.delete("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
