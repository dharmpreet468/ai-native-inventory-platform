import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.dependencies import get_current_user
from app.models.user import User


@pytest.fixture
def test_admin():
    """Provide a simulated admin for business-workflow tests."""
    return User(
        id=1,
        username="test_admin",
        email="test_admin@example.com",
        password_hash="test_password_hash",
        role="admin",
    )


@pytest.fixture
def authenticated_client(test_admin):
    """
    Provide an authenticated test client.

    The authentication override exists only during this fixture's lifetime.
    """
    previous_override = app.dependency_overrides.get(get_current_user)

    app.dependency_overrides[get_current_user] = lambda: test_admin

    try:
        with TestClient(app) as client:
            yield client
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_current_user, None)
        else:
            app.dependency_overrides[get_current_user] = previous_override