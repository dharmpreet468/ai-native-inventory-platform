from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
import jwt, uuid
from jwt.exceptions import InvalidTokenError

from app.core.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_SECRET_KEYS,
    JWT_REFRESH_TOKEN_EXPIRE_DAYS,
)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    payload = data.copy()

    now = datetime.now(timezone.utc)

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {"exp": expire, "iat": now, "jti": str(uuid.uuid4()), "type": "access"}
    )

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token


def create_refresh_token(data: dict) -> str:
    payload = data.copy()

    now = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    payload.update(
        {"exp": expire, "iat": now, "jti": str(uuid.uuid4()), "type": "refresh"}
    )

    return jwt.encode(payload, JWT_REFRESH_SECRET_KEYS, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid acess token type")

    return payload


def decode_refresh_token(token: str) -> dict:
    payload = jwt.decode(token, JWT_REFRESH_SECRET_KEYS, algorithms=JWT_ALGORITHM)

    if payload.get("type") != "refresh":
        raise InvalidTokenError("Invalid refresh token type")

    return payload
