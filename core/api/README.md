# Atlas Core API

FastAPI reference service that powers multi-tenant auth, billing stubs, and AI orchestration hooks.

## Features
- Tenant-aware dependency that reads `X-Atlas-Tenant` header.
- Health + metadata endpoints for CI smoke tests.
- Tenant CRUD + usage updates wired through `app/services/tenants.py`.
- Billing preview endpoint that simulates Stripe-ready pricing hooks.
- JWT auth (`/auth/token`) plus protected tenant/usage mutations.
- Stripe webhook placeholder (`/webhooks/stripe`) with signature validation.
- Usage metering endpoints (`/metrics/usage`, `/metrics/usage/daily`) storing events for analytics + cost alerts.
- Admin users live in the database (`adminuser` table). Update `ATLAS_AUTH_USERNAME`/`ATLAS_AUTH_PASSWORD` and rerun `alembic upgrade head` (or `seed_admin_user`) to rotate credentials consistently across environments.

## Getting Started
```bash
cd core/api
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
ATLAS_DATABASE_URL=sqlite:///atlas.db uvicorn app.main:app --reload
```

## Testing
```bash
pytest
```

Expose env vars shown in `app/config.py` (or create a `.env`) to adjust defaults. The `tests/` suite covers health checks, tenant flows, and billing previews. Use `ATLAS_DATABASE_URL=sqlite://` for in-memory testing or point at Postgres (see `docker-compose.yml`).

## Auth & Webhooks
- `POST /auth/token` expects `{ "username": "admin@atlas", "password": "atlas" }` by default and returns a bearer token (set `ATLAS_AUTH_*` to change).
- Include `Authorization: Bearer <token>` when calling `POST /tenants` or `POST /tenants/{id}/usage`.
- Mock Stripe events by sending JSON payloads to `POST /webhooks/stripe` with `Stripe-Signature: whsec_demo` (configurable via `ATLAS_STRIPE_WEBHOOK_SECRET`).
