import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No special setup needed, as activities are predefined in app.py
    
    # Act: Make the GET request
    response = client.get("/activities")
    
    # Assert: Check response status and structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange: Ensure the activity exists and email isn't already signed up
    activity_name = "Chess Club"
    email = "test@example.com"
    
    # Act: Perform the signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert: Check success response and that participant was added
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email} for {activity_name}" in data["message"]
    
    # Verify in the activities data
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate():
    # Arrange: Sign up once first
    activity_name = "Chess Club"
    email = "duplicate@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act: Attempt to sign up again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert: Check for error
    assert response.status_code == 400
    data = response.json()
    assert "Student is already signed up" in data["detail"]

def test_signup_invalid_activity():
    # Arrange: Use a non-existent activity
    invalid_activity = "Invalid Activity"
    email = "test@example.com"
    
    # Act: Try to sign up
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert: Check for 404 error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # Arrange: Sign up first so we can unregister
    activity_name = "Programming Class"
    email = "unregister@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act: Unregister the participant
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert: Check success and that participant was removed
    assert response.status_code == 200
    data = response.json()
    assert f"Unregistered {email} from {activity_name}" in data["message"]
    
    # Verify removal
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_signed_up():
    # Arrange: Use an email not signed up
    activity_name = "Chess Club"
    email = "notsigned@example.com"
    
    # Act: Try to unregister
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert: Check for error
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up" in data["detail"]

def test_unregister_invalid_activity():
    # Arrange: Use a non-existent activity
    invalid_activity = "Invalid Activity"
    email = "test@example.com"
    
    # Act: Try to unregister
    response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert: Check for 404 error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]