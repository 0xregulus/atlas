"""Qdrant helper client (mock-aware for local demos)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:  # pragma: no cover - optional dependency path
    from qdrant_client import QdrantClient  # type: ignore
    from qdrant_client.http import models as rest  # type: ignore
except Exception:  # pragma: no cover
    QdrantClient = None  # type: ignore
    rest = None  # type: ignore


@dataclass
class VectorClient:
    host: str | None = None
    api_key: str | None = None

    def _client(self) -> QdrantClient | None:
        if QdrantClient is None:
            return None
        return QdrantClient(host=self.host or "localhost", api_key=self.api_key)

    def ensure_collection(self, collection: str = "knowledge_base") -> None:
        client = self._client()
        if not client or rest is None:
            return
        client.recreate_collection(
            collection_name=collection,
            vectors_config=rest.VectorParams(size=768, distance=rest.Distance.COSINE),
        )

    def similarity_search(self, tenant: str, query: str, collection: str | None = None) -> list[dict[str, Any]]:
        # In scaffold mode we simply return canned docs so the rest of the graph can execute.
        docs = [
            {"id": "1", "content": f"Tenant {tenant} SOPs for {query}"},
            {"id": "2", "content": "Escalation path -> Slack #atlas-hitl"},
        ]
        return docs
