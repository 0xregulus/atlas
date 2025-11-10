from fastapi import APIRouter

from ..config import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", summary="Liveness probe")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready", summary="Readiness probe")
def ready() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ready", "environment": settings.environment}
