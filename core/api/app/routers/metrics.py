from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..security import get_current_user
from ..services import metrics as metrics_service

router = APIRouter(prefix="/metrics", tags=["metrics"])


class UsageEventRequest(BaseModel):
    tenant: str
    source: str = "ai-service"
    tokens: int = 0
    latency_ms: float | None = None


@router.post("/usage", summary="Record usage event", status_code=202)
def record_usage(
    req: UsageEventRequest,
    _: Annotated[str, Depends(get_current_user)],
) -> dict[str, str]:
    metrics_service.record_usage_event(
        tenant=req.tenant,
        source=req.source,
        tokens=req.tokens,
        latency_ms=req.latency_ms,
    )
    return {"status": "accepted"}


@router.get("/usage/daily", summary="Aggregate usage in the last 24h")
def usage_summary(
    _: Annotated[str, Depends(get_current_user)],
) -> list[dict[str, object]]:
    return metrics_service.summarize_usage()
