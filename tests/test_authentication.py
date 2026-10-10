import jwt
import pytest

from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.core.dependencies import get_current_user
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.models.user import User


client = TestClient(app)


# --------------------------------------------------
# Test helpers
# --------------------------------------------------

def create_test_user():
    user = MagicMock(spec=User)

    user.id = 1
    user.username = "testuser"
    user.email = "testuser@example.com"
    user.role = "employee"

    return user


def create_test_token(
    user_id="1",
    expires_delta=timedelta(minutes=30),
):
    payload = {
        "sub": user_id,
        "role": "employee",
        "exp": datetime.now(timezone.utc) + expires_delta,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


@pytest.fixture
def authenticated_client():
    user = create_test_user()

    app.dependency_overrides[get_current_user] = lambda: user

    yield client

    app.dependency_overrides.clear()


# --------------------------------------------------
# Test 1: Missing token
# --------------------------------------------------

def test_missing_token_returns_401():
    response = client.get("/auth/me")

    assert response.status_code == 401


# --------------------------------------------------
# Test 2: Valid authenticated user
# --------------------------------------------------

def test_valid_token_returns_user(authenticated_client):
    token = create_test_token()

    response = authenticated_client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == 1
    assert body["username"] == "testuser"
    assert body["email"] == "testuser@example.com"
    assert body["role"] == "employee"

    assert "password_hash" not in body


# --------------------------------------------------
# Test 3: Malformed token
# --------------------------------------------------

def test_malformed_token_returns_401():
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid.token.value"
        },
    )

    assert response.status_code == 401


# --------------------------------------------------
# Test 4: Expired token
# --------------------------------------------------

def test_expired_token_is_rejected():
    token = create_test_token(
        expires_delta=timedelta(seconds=-10)
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 401


# --------------------------------------------------
# Test 5: Token with invalid signature
# --------------------------------------------------

def test_invalid_signature_returns_401():
    payload = {
        "sub": "1",
        "role": "employee",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        "incorrect-test-signing-key-at-least-32-bytes",
        algorithm=JWT_ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 401


# --------------------------------------------------
# Test 6: Token without subject
# --------------------------------------------------

def test_token_without_subject_returns_401():
    payload = {
        "role": "employee",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 401