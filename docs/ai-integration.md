# AI Service Integration Notes

## Core API Contracts
- `GET /tenants/{id}/catalog` — determines which datasets LangGraph can retrieve; mapped in `ai/services/core_client.py`. Each dataset name should align with dbt outputs (`data/transformations/models`).
- `POST /tenants/{id}/usage` — future hook for LangGraph to push manual adjustments into billing (requires JWT).
- `GET /billing/{id}/preview` — surfaced in frontend to correlate AI usage and cost.
- `POST /metrics/usage` — LangGraph reports token burn + latency here when `ATLAS_AI_CORE_API_TOKEN` is provided; `GET /metrics/usage/daily` powers dashboards/cost alerts.

## Data Platform Hooks
- Airbyte syncs (see `data/ingestion/`) land in S3/DuckDB, dbt models materialize `fct_ai_context`, and `data/feature-store/tenant_context.yaml` exposes the contract for AI retrieval.
- `ai/vector_search/ingest.py` demonstrates how to load dbt outputs into Qdrant or a mock store, while `ai/services/core_client.py` now reports usage events back to the core API.

## Observability
- LangGraph evaluations (sentiment, hallucination risk) in `ai/agents/orchestrator.py` should be exported via OTLP (`ATLAS_AI_OTLP_ENDPOINT`). Coordinate with `infra/observability/` for dashboards (`grafana-dashboard.json`).
- HITL escalations reuse the channels orchestrated in `automation/` so product + ops share context.

Keep this document updated as you implement real pipelines so reviewers see the full story from source data to AI behavior.
