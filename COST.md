# Cost Strategy

Estimate monthly AWS spend for a seed-stage deployment. Update numbers once infra code is implemented.

| Layer | Service | Assumption | Est. Monthly |
| --- | --- | --- | --- |
| Compute | ECS/Fargate (2 prod + 1 staging svc) | t3.large @ 50% utilization | $420 |
| Data | RDS PostgreSQL Multi-AZ | db.m5.large | $380 |
| Storage | S3 (raw + curated) | 2 TB + lifecycle rules | $50 |
| AI | OpenAI / Anthropic APIs | 3M input / 1M output tokens | $500 |
| Vector | Qdrant Cloud | 3 small clusters | $270 |
| Observability | Grafana Cloud / Managed OSS | 400 GB logs + metrics | $150 |
| Automation | n8n Cloud + Slack integration | Pro tier | $40 |
| Misc | NAT, bandwidth, backups | best-effort buffer | $190 |

**Total ~ $2k/month** to support a serious demo/staging footprint. Production budgets should add 30-50% buffer for data growth, AI spikes, and regional redundancy.

## Guardrails
- Auto-shutdown preview environments after 12h of inactivity.
- Enforce token budgets per tenant; alert via Slack when >80% consumed.
- Turn on S3 lifecycle + Glacier deep archive for cold data.
- Track unit cost per active tenant inside `docs/product/strategy.md`.

## Dashboards & Alerts
- **Grafana Cost Overview:** Combine `/tenants/current` usage metrics with Stripe forecasts (from `billing/preview`) to show ARR vs consumption per plan tier.
- **AI Token Burn vs KPI:** Pull LangGraph evaluation logs (`ai/agents/orchestrator.py`) into the same dashboard so hallucination rates are viewed alongside spend.
- **Automated Actions:** When cost per tenant exceeds plan limits, trigger n8n workflow that pings the same HITL channel used by AI escalations (`ai/workflows/hitl.py`). Document the response in `automation/playbooks/`.
