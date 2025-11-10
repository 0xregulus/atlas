# Observability Blueprint

Atlas treats observability as a first-class product surface. The stack assumes:

- **Instrumentation:** FastAPI emits JSON logs via `RequestMetricsMiddleware` and can stream OTLP traces when `ATLAS_OTLP_ENDPOINT` is configured. LangGraph does the same via `ATLAS_AI_OTLP_ENDPOINT`.
- **Pipelines:** Fluent Bit/Vector ship logs to Loki; OTLP traces + metrics land in Tempo/Prometheus. GitHub Actions publishes deployment metadata to the same sinks so dashboards show code version + feature flag context.
- **Dashboards:** Grafana visualizes tenant-level latency, AI token spend, and cost guardrails. A k6/Playwright synthetic board keeps tabs on user journey KPIs.
- **Alerting:** Alertmanager/Graphite hooks route to Slack + n8n runbooks. Critical alerts require on-call ack + optional human-in-the-loop workflow (same channels the AI agents escalate to).

## Metrics to Track
- P95/P99 latency per tenant and per API route.
- AI token/request consumption vs plan limits (mirrors `billing` preview values).
- LangGraph agent success vs HITL escalations (source: `ai/agents` eval harness).
- ETL/data freshness for each dataset contract returned by `/tenants/{id}/catalog`.

## Next Actions
1. Wire OpenTelemetry FastAPI middleware + Resource detectors in `core/api/app/telemetry.py` and export OTLP to Grafana Cloud.
2. Add LangGraph evaluation spans (success/failure, hallucination score) so AI guardrails surface directly in Grafana.
3. Publish Terraform modules in `infra/observability/` for Loki, Tempo, and Grafana dashboards; point `docs/product/strategy.md` to the live URLs.

## Local Collector Quickstart
```bash
docker run --rm -p 4318:4318 \
  -v ${PWD}/infra/observability/otel-collector.yaml:/etc/otelcol/config.yaml \
  otel/opentelemetry-collector:0.96.0
```
Then set `ATLAS_OTLP_ENDPOINT` and/or `ATLAS_AI_OTLP_ENDPOINT` to `http://localhost:4318/v1/traces` (and metrics if applicable).

## Terraform Module
`infra/terraform/modules/observability` provisions:
- An optional Amazon Managed Prometheus workspace.
- An ECS Fargate service running the OpenTelemetry Collector (config rendered from `templates/otel-config.tpl`).

In `infra/terraform/main.tf`, fill in `subnet_ids` / `security_group_ids` before running:
```bash
cd infra/terraform
terraform init
terraform apply -var subnet_ids='["subnet-abc","subnet-def"]' -var security_group_ids='["sg-123"]'
```
Outputs include the Prometheus remote write endpoint you can wire into Grafana dashboards like `infra/observability/grafana-dashboard.json`.
