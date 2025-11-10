# ADR-001: Foundational Stack Selection
- **Status:** Accepted
- **Date:** 2024-05-01
- **Owners:** Atlas Platform Team

## Context
Atlas needs to demonstrate a modern yet pragmatic stack that hiring managers associate with high-performing SaaS+AI orgs. The stack must be cloud-ready, AI-friendly, and have strong community support.

## Decision
Adopt the following baseline:
- Next.js 15 + tRPC for the multi-tenant dashboard and admin experience.
- FastAPI services backed by PostgreSQL + Redis for transactional workloads.
- LangGraph + Qdrant for orchestrated RAG agents.
- Airbyte + DuckDB + dbt for the analytics/data foundation.
- Terraform + AWS CDK targeting ECS/Fargate for infra automation.

## Consequences
- **Positive:** Aligns with industry expectations, maximizes hiring signal, and keeps AI orchestration modular.
- **Negative:** Two IaC frameworks (Terraform + CDK) adds complexity; requires disciplined docs.
- **Follow-ups:** Document IaC ownership split and create golden paths for new modules.

## Alternatives Considered
1. **All-in on Serverless (Lambda, DynamoDB):** Simplifies ops but harder to showcase infra depth.
2. **Monorepo with Nx/NestJS everywhere:** Clean DX but less diverse toolkit for interviews.

## References
- `ARCHITECTURE.md`
- `docs/diagrams/atlas-high-level.mmd`
