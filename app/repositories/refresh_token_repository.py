import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create_token(self, user_id: int, token: str, expires_at: str) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id, token_hash=self.hash_token(token), expires_at=expires_at
        )
        self.db.add(refresh_token)
        self.db.flush()

        return refresh_token

    def get_by_token(self, token: str) -> RefreshToken | None:
        token_hash = self.hash_token(token)

        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)

        return self.db.execute(statement).scalar_one_or_none()

    def get_by_token_for_update(self, token: str) -> RefreshToken | None:
        token_hash = self.hash_token(token)

        statement = (
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .with_for_update()
        )

        return self.db.execute(statement).scalar_one_or_none()

    def revoke(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked = True
        self.db.flush()
