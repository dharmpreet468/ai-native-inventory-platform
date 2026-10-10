import jwt

from fastapi import Depends, HTTPException, status
from collections.abc import Callable
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.core.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        print("JWT decoded successfully")
        print("Token type:", payload.get("type"))
        print("Token subject:", payload.get("sub"))

        if payload.get("type") != "access":
            print("Rejected: incorrect token type")
            raise credentials_exception

        user_id = payload.get("sub")

        if user_id is None:
            print("Rejected: missing subject")
            raise credentials_exception

        user_id = int(user_id)

    except InvalidTokenError as exc:
        print("JWT validation error:", type(exc).__name__)
        raise credentials_exception

    except (ValueError, TypeError) as exc:
        print("JWT claim error:", type(exc).__name__)
        raise credentials_exception

    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)

    if user is None:
        print("Rejected: user not found")
        raise credentials_exception

    return user


def require_roles(*allowed_roles: str) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="You do not have permissions to perform this action",
            )

        return current_user

    return role_checker
