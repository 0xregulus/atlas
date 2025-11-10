# Atlas Architecture Notes

This document expands on the high-level diagram in `README.md` and explains the rationale behind each layer. Treat it as a living narrative that can be referenced during interviews or architecture reviews.

## 1. Frontend Experience
- Next.js 15 (app router) with Tailwind and Radix primitives for fast product iteration.
- tRPC used at the edge to keep type-safe contracts with the backend services, even when teams build separate vertical apps.
- Multi-tenant context is injected via middleware and is also used to scope feature flags and billing limits.

## 2. Core Services (FastAPI or NestJS)
- API gateway fans out to domain services (`users`, `billing`, `ledger`, `workflows`).
- Postgres acts as the system of record while Redis handles session + rate limiting.
- RBAC middleware enforces tenant isolation via policy-as-code (Open Policy Agent or custom rules).
- Event bus (Kafka / SNS+SQS) propagates domain events to data/AI pipelines without coupling deployments.

## 3. Data Platform
- Airbyte workloads land data into S3, then DuckDB materializes curated zones for analytics and ad hoc experimentation.
- dbt manages modeling, tests, and documentation; feature store exports train/inference-ready views.
- Cost guardrails rely on storage lifecycle policies + usage metrics exported via Prometheus.

## 4. AI & Automation Layer
- LangGraph orchestrates retrieval-augmented agent flows, decoupling prompts, tools, and safety rails.
- Qdrant hosts multi-tenant vector collections; semantic cache short-circuits repeated calls.
- Evaluation harness (OpenAI Evals / custom pytest suite) ensures regressions are caught before deploy.
- n8n workflows route ambiguous cases to Slack/Human approval, creating human-in-the-loop governance.

## 5. Infrastructure & Observability
- Terraform defines shared AWS foundations (networking, RDS, S3, queues) while CDK codifies higher-level app stacks.
- Deployment target: containerized services on ECS/Fargate (or EKS) with blue/green deployments.
- OpenTelemetry spans forward metrics/logs to Grafana/Loki; alerts flow into Slack or PagerDuty.

## 6. Delivery Lifecycle
1. Engineer opens PR → GitHub Actions runs lint/tests + infra plan.
2. Successful merges trigger staging deploy -> smoke tests -> manual/auto promotion.
3. n8n recipes coordinate incidents, migrations, or product rollouts.
4. Metrics + COST guardrails inform ROADMAP prioritization.

## Diagrams
- `docs/diagrams/atlas-high-level.mmd` — source for the overview diagram (editable via Mermaid).
- Future diagrams: data lineage, agent orchestration, tenancy model.

## Open Questions / TODO
- Select definitive stack combo (FastAPI vs NestJS) and document trade-off in an ADR.
- Capture SLAs + SLOs per tenant tier.
- Add threat modeling notes for AI features (prompt injection, data exfiltration).
