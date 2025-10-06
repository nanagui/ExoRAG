"""JWT authentication utilities and dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from .config import get_settings

security = HTTPBearer(auto_error=False)


class User(BaseModel):
    username: str
    roles: list[str] = []


def create_access_token(
    *,
    subject: str,
    roles: Iterable[str],
    expires_delta: timedelta | None = None,
) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=4))
    payload = {
        "sub": subject,
        "roles": list(roles),
        "exp": expire,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")

    token = credentials.credentials
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    username = payload.get("sub")
    roles = payload.get("roles", [])
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return User(username=username, roles=list(roles))


def require_roles(*required_roles: str):
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if required_roles and not any(role in user.roles for role in required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return dependency


__all__ = ["User", "create_access_token", "get_current_user", "require_roles"]
