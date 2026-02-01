from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None):
    """Returns a new access token with user's data/"""
    payload = data.copy()
    if expires_delta is not None:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    payload.update({"exp": expires})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, ALGORITHM)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)
