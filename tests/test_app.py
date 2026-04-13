import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]


def test_signup_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    # Ensure user is signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_success():
    email = "testuser3@mergington.edu"
    activity = "Gym Class"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]


def test_unregister_not_found():
    email = "notfound@mergington.edu"
    activity = "Art Club"
    # Ensure user is not signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_activity_not_found():
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 404
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404
