"""Semantic cache scaffold used by the LangGraph orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass
class CacheEntry:
    response: str
    context: str


class SemanticCache:
    def __init__(self) -> None:
        self._entries: Dict[Tuple[str, str], CacheEntry] = {}

    def get(self, tenant: str, question: str) -> CacheEntry | None:
        return self._entries.get((tenant, question))

    def set(self, tenant: str, question: str, *, response: str, context: str) -> None:
        self._entries[(tenant, question)] = CacheEntry(response=response, context=context)

    def clear(self) -> None:
        self._entries.clear()


cache = SemanticCache()
