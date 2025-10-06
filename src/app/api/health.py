"""Health and metrics endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ..config import get_settings

router = APIRouter()


@router.get("/health", summary="Service health check")
async def health_check() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name}
