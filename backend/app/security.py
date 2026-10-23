"""Password hashing and JWT helpers.

Kept separate from the routes so they can be unit-tested on their own
and reused anywhere (Single Responsibility).
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings


def hash_password(plain_password: str) -> str:
    # bcrypt adds a random salt, so the same password hashes differently each time.
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(user_id: int, expires_in_minutes: int | None = None) -> str:
    minutes = expires_in_minutes if expires_in_minutes is not None else settings.token_expiry_minutes
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int | None:
    """Return the user id inside a valid token, or None if it's expired/tampered."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None