from fastapi.testclient import TestClient
import pytest
import uuid
from main import app
from database import SessionLocal
from models import User
from auth import hash_password
@pytest.fixture(scope="session", autouse=True)
def create_test_users():
    db = SessionLocal()

    users = [
        User(
            username="pytestuser",
            email="pytestuser@example.com",
            hashed_password=hash_password("Test@123"),
            role="user",
        ),
        User(
            username="user1",
            email="user1@example.com",
            hashed_password=hash_password("User@123"),
            role="user",
        ),
        User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("Admin@123"),
            role="admin",
        ),
    ]

    for user in users:
        existing = db.query(User).filter(
            User.username == user.username
        ).first()

        if not existing:
            db.add(user)

    db.commit()
    db.close()

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Incident Management API is running"
    }

def test_get_incidents_without_token():
    response = client.get("/incidents")

    assert response.status_code == 401

def test_register_user():
    username = f"pytestuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    response = client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@123"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == username

def test_login():
    response = client.post(
        "/login",
        data={
            "username": "pytestuser",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_incidents_with_token():
    login_response = client.post(
        "/login",
        data={
            "username": "pytestuser",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/incidents",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_normal_user_cannot_delete_incident():
    login_response = client.post(
        "/login",
        data={
            "username": "user1",
            "password": "User@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        "/incidents/6",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

def test_admin_can_delete_incident():
    login_response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "Admin@123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/incidents",
        json={
            "title": "Test incident",
            "description": "Incident created for testing",
            "priority": "Low",
            "status": "Open"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    incident_id = create_response.json()["id"]

    response = client.delete(
        f"/incidents/{incident_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_create_incident():
    login_response = client.post(
        "/login",
        data={
            "username": "user1",
            "password": "User@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/incidents",
        json={
            "title": "Test API incident",
            "description": "Created during automated testing",
            "priority": "High",
            "status": "Open"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test API incident"

def test_filter_incidents_by_status():
    login_response = client.post(
        "/login",
        data={
            "username": "user1",
            "password": "User@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/incidents?status=Open",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    for incident in response.json():
        assert incident["status"] == "Open"

def test_incident_pagination():
    login_response = client.post(
        "/login",
        data={
            "username": "user1",
            "password": "User@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/incidents?skip=0&limit=2",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) <= 2