from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.models.user import User


def test_user_registration_success_and_duplicate_rejection():
    """
    Verify that:
    1. A new user can register.
    2. The user receives the default employee role.
    3. The password is stored as a hash, not plaintext.
    4. Duplicate username registration is rejected.
    5. Duplicate email registration is rejected.
    """

    unique_id = uuid4().hex[:12]

    username = f"register_test_{unique_id}"
    email = f"{username}@example.com"
    password = "SecureTestPassword123!"

    with TestClient(app) as client:

        # --------------------------------------------------
        # 1. Register a new user
        # --------------------------------------------------

        registration_response = client.post(
            "/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
            },
        )

        assert registration_response.status_code in (200, 201), (
            f"Registration failed: {registration_response.status_code}, "
            f"{registration_response.text}"
        )

        registration_data = registration_response.json()

        assert registration_data["username"] == username
        assert registration_data["email"] == email
        assert registration_data["role"] == "employee"
        assert "id" in registration_data

        # The API must not return the password or password hash.
        assert "password" not in registration_data
        assert "password_hash" not in registration_data

        # --------------------------------------------------
        # 2. Verify the user is persisted correctly
        # --------------------------------------------------

        db_generator = get_db()
        db = next(db_generator)

        try:
            user = (
                db.query(User)
                .filter(User.username == username)
                .first()
            )

            assert user is not None
            assert user.email == email
            assert user.role == "employee"

            # Never store the plaintext password.
            assert user.password_hash != password

            # Verify that the stored hash validates the password.
            from app.core.security import verify_password

            assert verify_password(password, user.password_hash)

        finally:
            db.close()
            try:
                next(db_generator)
            except StopIteration:
                pass

        # --------------------------------------------------
        # 3. Reject duplicate username
        # --------------------------------------------------

        duplicate_username_response = client.post(
            "/auth/register",
            json={
                "username": username,
                "email": f"another_{unique_id}@example.com",
                "password": password,
            },
        )

        assert duplicate_username_response.status_code == 409, (
            "Registration with an existing username should return 409"
        )

        # --------------------------------------------------
        # 4. Reject duplicate email
        # --------------------------------------------------

        duplicate_email_response = client.post(
            "/auth/register",
            json={
                "username": f"another_{unique_id}",
                "email": email,
                "password": password,
            },
        )

        assert duplicate_email_response.status_code == 409, (
            "Registration with an existing email should return 409"
        )