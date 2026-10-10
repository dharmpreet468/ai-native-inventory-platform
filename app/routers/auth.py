from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
)

from app.services.auth_services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)

    user = auth_service.register(data)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)

    return auth_service.login(data)


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(data: RefreshRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)

    return auth_service.refresh_token(data)


@router.get("/me")
def get_authenticated_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }
