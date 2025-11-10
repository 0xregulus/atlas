from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from sqlmodel import select, func

from ..database import get_session
from ..models import UsageEvent


def record_usage_event(*, tenant: str, source: str, tokens: int, latency_ms: float | None) -> UsageEvent:
    event = UsageEvent(
        tenant_id=tenant,
        source=source,
        tokens=tokens,
        latency_ms=latency_ms,
    )
    with get_session() as session:
        session.add(event)
        session.commit()
        session.refresh(event)
    return event


def get_usage_events_since(hours: int = 24) -> Iterable[UsageEvent]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with get_session() as session:
        statement = select(UsageEvent).where(UsageEvent.created_at >= cutoff)
        for row in session.exec(statement):
            yield row


def summarize_usage(hours: int = 24) -> list[dict[str, object]]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with get_session() as session:
        statement = (
            select(
                UsageEvent.tenant_id,
                func.count(UsageEvent.id).label("events"),
                func.sum(UsageEvent.tokens).label("tokens"),
                func.avg(UsageEvent.latency_ms).label("latency_ms"),
            )
            .where(UsageEvent.created_at >= cutoff)
            .group_by(UsageEvent.tenant_id)
        )
        results = []
        for row in session.exec(statement):
            results.append(
                {
                    "tenant": row.tenant_id,
                    "events": int(row.events or 0),
                    "tokens": int(row.tokens or 0),
                    "latency_ms": float(row.latency_ms or 0.0),
                    "window_hours": hours,
                }
            )
        return results
