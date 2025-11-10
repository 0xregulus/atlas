"""Telemetry helpers for the Atlas Core API."""

from __future__ import annotations

import json
import logging
import os
from time import perf_counter
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

_LOG_LEVEL = os.getenv("ATLAS_LOG_LEVEL", "INFO")
logger = logging.getLogger("atlas.core")
_OTLP_ENDPOINT = os.getenv("ATLAS_OTLP_ENDPOINT")


def configure_logging() -> None:
    if logger.handlers:
        return
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(_LOG_LEVEL)
    if _OTLP_ENDPOINT:
        provider = TracerProvider()
        processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=_OTLP_ENDPOINT))
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)


class RequestMetricsMiddleware(BaseHTTPMiddleware):
    """Lightweight middleware that emits JSON logs for every request."""

    async def dispatch(self, request: Request, call_next: Callable):  # type: ignore[override]
        start = perf_counter()
        response = await call_next(request)
        duration_ms = round((perf_counter() - start) * 1000, 2)
        payload = {
            "event": "api_request",
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "tenant": request.headers.get("X-Atlas-Tenant"),
        }
        logger.info(json.dumps(payload))
        return response
