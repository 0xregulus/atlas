# Atlas Roadmap

## 0-30 Days (MVP)
- Ship FastAPI auth/billing skeleton with tenant-aware RBAC.
- Stand up Qdrant + LangGraph sandbox connected to sample knowledge base.
- Terraform baseline (VPC, RDS, S3, ECS) with CI plan stage.
- Publish first ADRs + strategy narrative; record Loom vision demo.

## 30-60 Days (Execution)
- Add dbt semantic layer + feature store preview APIs.
- Wire GitHub Actions to deploy infra + app containers automatically.
- Integrate n8n workflow for human-in-the-loop escalations.
- Implement Observability dashboards + cost alerts.

## 60-90 Days (Scale)
- Introduce tenant-tier SLAs and automated usage metering.
- Launch plugin/extension story (Atlas Platform variant).
- Harden AI eval pipeline with synthetic + real feedback loops.
- Add load/perf tests (k6 + Playwright) to CI.

## North Star
- Self-serve onboarding for new tenants within 1 hour.
- AI copilots with measurable ROI metrics per persona.
- Infra guardrails that keep unit cost flat while usage grows 3x.
