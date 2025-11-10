# AI Services

This folder captures the LangGraph-based orchestration layer and supporting assets.

## Subdirectories
- `agents/` — multi-agent graphs, tool definitions, evaluation harness.
- `vector_search/` — Qdrant schemas, migration scripts, seed embeddings.
- `prompts/` — prompt templates, guardrails, semantic cache configuration.
- `workflows/` — playbooks for human-in-the-loop review, escalation policies.

## CLI
```bash
cd ai
uv pip install -e .[dev]
python -m ai.service run "How do I ship an AI demo?" --tenant demo
```

The CLI uses `ai/config.py` for environment variables (`ATLAS_AI_CORE_API_URL`, etc.) and prints LangGraph state + evaluation metrics.

## Quick Start
```bash
cd ai
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
python -m ai.examples.simulate_agent
```

The script wires `ai/agents/orchestrator.py` (LangGraph) to `ai/workflows/hitl.py` to showcase human-in-the-loop automation.

### Optional: Live Qdrant
Start Qdrant via `docker compose up qdrant` (root-level compose file). Update `ATLAS_AI_QDRANT_URL` in your environment and run `python -m ai.vector_search.ingest data/sample_fct_ai_context.json --tenant demo` once you have dbt output available.

### Reporting Usage
- Set `ATLAS_AI_CORE_API_TOKEN` to the JWT issued by `/auth/token` (and ensure `ATLAS_AI_CORE_API_URL` points at your FastAPI instance).
- When configured, every LangGraph run posts to `POST /metrics/usage` so the core API can aggregate AI tokens + latency for billing/observability dashboards.

## Next Tasks
- Replace the mocked Qdrant client with a live deployment and add migrations.
- Connect `ai/config.py` to the core API (`/tenants/{id}/catalog`) to hydrate retrieval data.
- Export evaluation metrics + semantic cache hits via OpenTelemetry for Grafana dashboards.
