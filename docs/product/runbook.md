# Atlas Local Runbook

## Prereqs
- Python 3.14 (or 3.11+) with `uv` for environment management.
- Node.js 20+ (pnpm or npm).
- Docker (optional) for Postgres/Qdrant.

## Steps
1. **Core API**
   ```bash
   cd core/api
   uv venv .venv --python 3.14
   uv pip install -e .[dev]
   alembic upgrade head
   ATLAS_ENVIRONMENT=local ATLAS_DATABASE_URL=sqlite:///atlas.db CORE_API_URL=http://localhost:8000 uvicorn app.main:app --reload
   ```
   (Optionally override `ATLAS_AUTH_USERNAME`, `ATLAS_AUTH_PASSWORD`, or `ATLAS_AUTH_SECRET` before issuing tokens.)
   - Admin users live in the `adminuser` table; rerun `alembic upgrade head` (or call `seed_admin_user`) whenever you rotate credentials so CI/compose stay in sync.
2. **Frontend**
   ```bash
   cd frontend
   npm install
   NEXT_PUBLIC_CORE_API_URL=http://localhost:8000 CORE_API_URL=http://localhost:8000 CORE_API_BEARER_TOKEN=$(curl -s -X POST http://localhost:8000/auth/token -H 'Content-Type: application/json' -d '{"username":"admin@atlas","password":"atlas"}' | jq -r .access_token) npm run dev
   ```
3. **AI Services**
   ```bash
   cd ai
   uv venv .venv --python 3.14
   uv pip install -e .[dev]
   python -m ai.service run "How do I launch a demo?" --tenant demo
   ```
   Optional: run `python -m ai.examples.simulate_agent` to emit HITL logs.
4. **Data/dbt**
   ```bash
   cd data/transformations
   dbt run --select marts
   ```
   (Use `data/ingestion/airbyte_connection_knowledge_base.json` to configure Airbyte.)
5. **Telemetry**
   - Tail FastAPI logs (JSON) or export to OTLP collector.
   - Use `infra/terraform` to provision Grafana/Loki once ready.
   - Set `ATLAS_OTLP_ENDPOINT` (core API) and `ATLAS_AI_OTLP_ENDPOINT` (LangGraph) to ship traces/metrics via OTLP HTTP exporters.
   - Local collector: `docker run --rm -p 4318:4318 -v $(pwd)/infra/observability/otel-collector.yaml:/etc/otelcol/config.yaml otel/opentelemetry-collector:0.96.0`.

## Docker Compose Shortcut
```bash
CORE_API_BEARER_TOKEN=$(curl -s -X POST http://localhost:8000/auth/token \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin@atlas","password":"atlas"}' | jq -r .access_token) \
  docker compose up --build
```
This starts Postgres, Qdrant, the FastAPI service, and the Next.js frontend. Env vars are pre-wired for local networking (`core-api`, `frontend`). Update `docker-compose.yml` if you want to add LangGraph workers or observability collectors.

To run migrations inside the Compose stack before the first boot (the CI pipeline runs the same command):
```bash
docker compose run --rm core-api alembic upgrade head
```

## API Testing
- Import `docs/api/atlas.postman_collection.json` and `docs/api/atlas.postman_environment.json` into Postman/Bruno. First run **Auth Token** to populate `authToken`, then exercise protected endpoints (tenant upsert/usage) or the Stripe webhook.
- Run **Record Usage Event** followed by **Usage Summary** to verify the AI metering flow is live.
- Alternatively run `curl` commands or add these requests to your CI smoke suite.

## Smoke Tests
- `curl http://localhost:8000/tenants/current` should return usage.
- Frontend dashboard updates after clicking **Simulate Usage**.
- `cd ai && PYTHONPATH=.. .venv/bin/python -m pytest` ensures LangGraph + cache behave (set `TMPDIR` if needed).
