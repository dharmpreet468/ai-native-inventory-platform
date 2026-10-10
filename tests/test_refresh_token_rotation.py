from fastapi.testclient import TestClient

from app.main import app


def test_refresh_token_rotation_and_replay_protection():
    """
    Verify that:
    1. Login issues access and refresh tokens.
    2. A valid refresh token can be used once.
    3. The old refresh token is rejected after rotation.
    4. The replacement refresh token works.
    5. The replacement token is also rotated and cannot be reused.
    """

    with TestClient(app) as client:

        # --------------------------------------------------
        # 1. Register a unique test user
        # --------------------------------------------------

        import uuid

        unique_id = uuid.uuid4().hex[:12]

        username = f"refresh_test_{unique_id}"
        email = f"{username}@example.com"
        password = "TestPassword123!"

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

        # --------------------------------------------------
        # 2. Log in and obtain the original refresh token
        # --------------------------------------------------

        login_response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        login_data = login_response.json()

        original_refresh_token = login_data["refresh_token"]

        assert login_data["access_token"]
        assert original_refresh_token

        # --------------------------------------------------
        # 3. Refresh successfully using the original token
        # --------------------------------------------------

        first_refresh_response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": original_refresh_token,
            },
        )

        assert first_refresh_response.status_code == 200, (
            "A valid refresh token should be accepted"
        )

        first_refresh_data = first_refresh_response.json()

        replacement_refresh_token = first_refresh_data["refresh_token"]

        assert first_refresh_data["access_token"]
        assert replacement_refresh_token

        assert replacement_refresh_token != original_refresh_token

        # --------------------------------------------------
        # 4. Replay the original token
        # --------------------------------------------------

        replay_response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": original_refresh_token,
            },
        )

        assert replay_response.status_code == 401, (
            "The old refresh token must be rejected after rotation"
        )

        # --------------------------------------------------
        # 5. Verify the replacement token is still valid
        # --------------------------------------------------

        second_refresh_response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": replacement_refresh_token,
            },
        )

        assert second_refresh_response.status_code == 200, (
            "The replacement refresh token should remain valid"
        )

        second_refresh_data = second_refresh_response.json()

        second_replacement_token = second_refresh_data["refresh_token"]

        assert second_refresh_data["access_token"]
        assert second_replacement_token

        assert second_replacement_token != replacement_refresh_token

        # --------------------------------------------------
        # 6. Replay the second token after its rotation
        # --------------------------------------------------

        second_replay_response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": replacement_refresh_token,
            },
        )

        assert second_replay_response.status_code == 401, (
            "A rotated refresh token must not be reusable"
        )