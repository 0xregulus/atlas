from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import get_settings

settings = get_settings()
auth_scheme = HTTPBearer(auto_error=False)


import hashlib


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_access_token_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.auth_secret, algorithm=settings.auth_algorithm)


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.auth_secret, algorithms=[settings.auth_algorithm])
    except jwt.PyJWTError as exc:  # type: ignore[attr-defined]
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return sub


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
) -> str:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    return decode_token(credentials.credentials)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed
