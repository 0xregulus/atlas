from __future__ import annotations

import hashlib

from sqlmodel import select

from ..config import get_settings
from ..database import get_session
from ..models import AdminUser

settings = get_settings()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed_admin_user() -> None:
    hashed = hash_password(settings.auth_password)
    with get_session() as session:
        user = session.exec(select(AdminUser).where(AdminUser.username == settings.auth_username)).first()
        if not user:
            session.add(AdminUser(username=settings.auth_username, password_hash=hashed))
        else:
            if user.password_hash != hashed:
                user.password_hash = hashed
        session.commit()


def get_admin_user(username: str) -> AdminUser | None:
    with get_session() as session:
        return session.exec(select(AdminUser).where(AdminUser.username == username)).first()
