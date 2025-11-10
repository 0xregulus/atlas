"""Ingest dbt outputs into Qdrant (or mock store)."""

from __future__ import annotations

import json
from pathlib import Path

from .client import VectorClient


def ingest_from_file(path: Path, tenant: str, collection: str = "knowledge_base") -> None:
    client = VectorClient()
    rows = json.loads(path.read_text())
    for row in rows:
        client.similarity_search(tenant=tenant, query=row.get("dataset_name", ""), collection=collection)


if __name__ == "__main__":
    ingest_from_file(Path("data/sample_fct_ai_context.json"), tenant="demo")
