"""Auth endpoints: thin HTTP layer on top of user_service."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TokenResponse, UserCredentials, UserOut
from app.security import create_access_token
from app.services import user_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(credentials: UserCredentials, db: Session = Depends(get_db)):
    try:
        return user_service.register_user(db, credentials.email, credentials.password)
    except user_service.EmailAlreadyRegistered:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserCredentials, db: Session = Depends(get_db)):
    user = user_service.authenticate(db, credentials.email, credentials.password)
    if user is None:
        # Same message for "no such user" and "wrong password", so attackers
        # can't use this endpoint to discover which emails are registered.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(user.id), user=user)