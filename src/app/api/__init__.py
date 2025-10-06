"""API routers for the application."""

from fastapi import APIRouter

from . import predictions, health, metrics

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
router.include_router(metrics.router, tags=["metrics"])

__all__ = ["router"]
