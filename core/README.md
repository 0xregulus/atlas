# Core Services

Scope: authentication, tenant isolation, billing, and governance APIs.

## Subdirectories
- `api/` — FastAPI/NestJS routers, OpenAPI specs, tRPC procedures.
- `auth/` — OAuth providers, JWT issuance, session management, audit trails.
- `billing/` — Stripe integration, metering, invoices, cost allocation.
- `rbac/` — Policy definitions (OPA/Rego) + enforcement middleware.

## Next Tasks
- Model tenant + workspace entities and persist to Postgres.
- Stand up Stripe test harness + webhook receiver.
- Capture ADR for RBAC approach (attribute vs role-based).
- Generate seed data + fixtures for demos.
- Extend metrics endpoints (`/metrics/usage*`) with Prometheus/OTLP exporters and connect them to cost guardrails.
