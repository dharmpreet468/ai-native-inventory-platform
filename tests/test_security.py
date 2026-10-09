import jwt

from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def test_password_hashing():
    password = "TestPassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPassword", hashed_password)


def test_create_access_token():
    token = create_access_token({
        "sub": "1",
        "role": "employee",
    })

    assert isinstance(token, str)

    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )

    assert payload["sub"] == "1"
    assert payload["role"] == "employee"
    assert "exp" in payload