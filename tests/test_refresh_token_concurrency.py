from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_concurrent_refresh_requests_allow_only_one_success():
    """
    Two concurrent requests use the same refresh token.

    Expected:
    - Exactly one request succeeds.
    - The other request is rejected.
    - The original refresh token cannot be reused afterward.
    """

    # Create a unique user for this test.
    unique_id = uuid4().hex[:12]

    username = f"concurrent_test_{unique_id}"
    email = f"{username}@example.com"
    password = "TestPassword123!"

    # Use the application to register and log in.
    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
            },
        )

        assert register_response.status_code in (200, 201), (
            f"Registration failed: {register_response.status_code}"
        )

        login_response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        original_refresh_token = login_response.json()["refresh_token"]

    # Both worker threads wait at the barrier before making requests.
    start_barrier = Barrier(2)

    def refresh_request():
        # Each worker uses its own TestClient.
        with TestClient(app) as client:
            start_barrier.wait(timeout=10)

            return client.post(
                "/auth/refresh",
                json={
                    "refresh_token": original_refresh_token,
                },
            )

    # Execute both requests concurrently.
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_one = executor.submit(refresh_request)
        future_two = executor.submit(refresh_request)

        response_one = future_one.result(timeout=30)
        response_two = future_two.result(timeout=30)

    statuses = [
        response_one.status_code,
        response_two.status_code,
    ]

    # Exactly one request must succeed.
    assert statuses.count(200) == 1, (
        f"Expected exactly one successful refresh; got {statuses}"
    )

    # The other request must be rejected.
    assert statuses.count(401) == 1, (
        f"Expected exactly one rejected refresh; got {statuses}"
    )

    # Confirm the original token cannot be reused.
    with TestClient(app) as client:
        replay_response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": original_refresh_token,
            },
        )

    assert replay_response.status_code == 401, (
        "The original refresh token must remain revoked"
    )