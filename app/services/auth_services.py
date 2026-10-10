from datetime import datetime, timedelta, timezone

from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import JWT_REFRESH_TOKEN_EXPIRE_DAYS
from app.core.exceptions import (
    UsernameAlreadyExistedException,
    EmailAlreadyExistedException,
    InvalidUsernamePasswordException,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshRequest,
)


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.refresh_token_repository = RefreshTokenRepository(db)

    # --------------------------------------------------
    # REGISTER
    # --------------------------------------------------

    def register(self, data: RegisterRequest) -> User:

        existing_username = self.user_repository.get_by_username(
            data.username
        )

        if existing_username:
            raise UsernameAlreadyExistedException(
                username=data.username
            )

        existing_email = self.user_repository.get_by_email(
            data.email
        )

        if existing_email:
            raise EmailAlreadyExistedException(
                email=data.email
            )

        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
            role="employee",
        )

        try:
            self.user_repository.create_user(user)
            self.db.commit()
            self.db.refresh(user)

        except Exception:
            self.db.rollback()
            raise

        return user

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    def login(self, data: LoginRequest) -> dict[str, str]:

        user = self.user_repository.get_by_username(
            data.username
        )

        if not user:
            raise InvalidUsernamePasswordException()

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise InvalidUsernamePasswordException()

        token_data = {
            "sub": str(user.id),
            "role": user.role,
        }

        # Generate different token types.
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )

        try:
            self.refresh_token_repository.create_token(
                user_id=user.id,
                token=refresh_token,
                expires_at=expires_at.isoformat(),
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # --------------------------------------------------
    # REFRESH TOKEN ROTATION
    # --------------------------------------------------

    def refresh_token(
        self,
        data: RefreshRequest,
    ) -> dict[str, str]:

        credentials_exception = InvalidUsernamePasswordException()

        # 1. Validate refresh-token signature, expiration and type.
        try:
            payload = decode_refresh_token(
                data.refresh_token
            )

            user_id = int(payload["sub"])

        except (
            InvalidTokenError,
            ValueError,
            TypeError,
            KeyError,
        ):
            raise credentials_exception

        try:
            # 2. Lock and retrieve the stored refresh-token record.
            stored_token = (
                self.refresh_token_repository.get_by_token_for_update(
                    data.refresh_token
                )
            )

            if stored_token is None or stored_token.revoked:
                raise credentials_exception

            # 3. Validate database expiration.
            now = datetime.now(timezone.utc)
            expires_at = stored_token.expires_at

            # MySQL may return a naive datetime.
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(
                    tzinfo=timezone.utc
                )

            if expires_at <= now:
                stored_token.revoked = True
                self.db.commit()
                raise credentials_exception

            # 4. Ensure the JWT subject matches the database record.
            if stored_token.user_id != user_id:
                raise credentials_exception

            # 5. Confirm that the user still exists.
            user = self.user_repository.get_by_id(user_id)

            if user is None:
                raise credentials_exception

            token_data = {
                "sub": str(user.id),
                "role": user.role,
            }

            # 6. Generate a new access token and refresh token.
            new_access_token = create_access_token(token_data)
            new_refresh_token = create_refresh_token(token_data)

            new_expires_at = now + timedelta(
                days=JWT_REFRESH_TOKEN_EXPIRE_DAYS
            )

            # 7. Revoke the old refresh token.
            self.refresh_token_repository.revoke(
                stored_token
            )

            # 8. Persist the replacement refresh token.
            self.refresh_token_repository.create_token(
                user_id=user.id,
                token= new_refresh_token,
                expires_at=new_expires_at.isoformat(),
            )

            # 9. Commit rotation as one transaction.
            self.db.commit()

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer",
            }

        except InvalidUsernamePasswordException:
            raise

        except Exception:
            self.db.rollback()
            raise