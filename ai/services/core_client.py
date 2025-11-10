"""Client for interacting with the Atlas core API."""

from __future__ import annotations

from typing import Any

import httpx

from ..config import get_settings


def _auth_headers() -> dict[str, str]:
    settings = get_settings()
    if settings.core_api_token:
        return {"Authorization": f"Bearer {settings.core_api_token}"}
    return {}


def get_catalog(tenant: str) -> list[dict[str, Any]]:
    settings = get_settings()
    url = f"{settings.core_api_url}/tenants/{tenant}/catalog"
    try:
        response = httpx.get(url, timeout=5)
        response.raise_for_status()
        payload = response.json()
        return payload if isinstance(payload, list) else payload.get("datasets", [])
    except Exception:
        # Fall back to static contracts if API unavailable
        return [
            {"name": "knowledge_base", "description": "Fallback docs", "freshness": "unknown"},
            {"name": "sales_notes", "description": "Fallback notes", "freshness": "unknown"},
        ]


def report_usage_event(tenant: str, *, tokens: int, latency_ms: float | None) -> None:
    settings = get_settings()
    if not settings.core_api_token:
        return
    url = f"{settings.core_api_url}/metrics/usage"
    try:
        httpx.post(
            url,
            headers={**_auth_headers(), "Content-Type": "application/json"},
            json={
                "tenant": tenant,
                "source": "ai-service",
                "tokens": tokens,
                "latency_ms": latency_ms,
            },
            timeout=5,
        )
    except Exception:
        pass
