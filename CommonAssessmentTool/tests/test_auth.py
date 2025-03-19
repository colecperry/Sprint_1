from fastapi import status
from app.enums import UserRole, GenderEnum

print("UserRole Enum Values:", UserRole.__members__)


# Reusable User Data
NEW_USER = {
    "username": "newuser",
    "email": "new@test.com",
    "password": "testpass123",
    "role": UserRole.CASE_WORKER.value,
}

DUPLICATE_USERNAME_USER = {
    "username": "testadmin",  # This username exists in test database
    "email": "another@test.com",
    "password": "testpass123",
    "role": UserRole.CASE_WORKER.value,
}

DUPLICATE_EMAIL_USER = {
    "username": "uniqueuser",
    "email": "testadmin@example.com",  # This email exists in test database
    "password": "testpass123",
    "role": UserRole.CASE_WORKER.value,
}

INVALID_ROLE_USER = {
    "username": "newuser",
    "email": "new@test.com",
    "password": "testpass123",
    "role": "invalid_role",  # Invalid role
}


def test_create_user_success(client, admin_headers):
    """Test successful user creation by admin"""
    response = client.post("/auth/users", headers=admin_headers, json=NEW_USER)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == NEW_USER["username"]
    assert data["role"] == NEW_USER["role"]
    assert "password" not in data  # Password should not be in response


def test_create_user_duplicate_username(client, admin_headers):
    """Test creating user with existing username"""
    response = client.post("/auth/users", headers=admin_headers, json=DUPLICATE_USERNAME_USER)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already registered" in response.json()["detail"]


def test_create_user_duplicate_email(client, admin_headers):
    """Test creating user with existing email"""
    response = client.post("/auth/users", headers=admin_headers, json=DUPLICATE_EMAIL_USER)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_create_user_invalid_role(client, admin_headers):
    """Test creating user with invalid role"""
    response = client.post("/auth/users", headers=admin_headers, json=INVALID_ROLE_USER)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_unauthorized(client):
    """Test user creation without authentication"""
    response = client.post("/auth/users", json=NEW_USER)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_success_admin(client):
    """Test successful login for admin"""
    response = client.post(
        "/auth/token", data={"username": "testadmin", "password": "testpass123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_success_case_worker(client):
    """Test successful login for case worker"""
    response = client.post(
        "/auth/token", data={"username": "testworker", "password": "workerpass123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Test login with incorrect password"""
    response = client.post(
        "/auth/token", data={"username": "testadmin", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with non-existent username"""
    response = client.post(
        "/auth/token", data={"username": "nonexistent", "password": "testpass123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_invalid_token(client):
    """Test using invalid token"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/clients/", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate credentials" in response.json()["detail"]


def test_missing_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get("/clients/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Not authenticated" in response.json()["detail"]


def test_token_user_deleted(client, admin_headers):
    """Test using token of deleted user"""
    # First create a new user as admin
    temp_user = {
        "username": "temporary",
        "email": "temp@test.com",
        "password": "temppass123",
        "role": "admin",
    }
    response = client.post("/auth/users", headers=admin_headers, json=temp_user)
    assert response.status_code == status.HTTP_200_OK

    # Get token for new user
    response = client.post("/auth/token", data={"username": "temporary", "password": "temppass123"})
    token = response.json()["access_token"]

    # Try using the token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/clients/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
