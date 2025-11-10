# Data Platform

Defines ingestion, transformation, analytics, and feature store patterns.

## Subdirectories
- `ingestion/` — Airbyte connectors, schedule manifests, landing-zone policies.
- `transformations/` — dbt models, tests, and macros.
- `analytics/` — dashboards, KPI definitions, LookML/Metrics Layer specs.
- `feature-store/` — offline/online feature definitions, materialization jobs.

## Quick Start
```bash
cd data/transformations
dbt deps && dbt run --select marts
```

- Configure a `profiles.yml` pointing at DuckDB/Snowflake/etc.
- Use `data/ingestion/airbyte_connection_knowledge_base.json` as the template for Airbyte → S3 syncs.
- `feature-store/tenant_context.yaml` documents how dbt outputs feed AI services & billing dashboards.

## Next Tasks
- Author sample Airbyte connection config + secrets template.
- Create dbt project skeleton with staging + mart layers.
- Specify contract between feature store outputs and AI services.
- Capture data governance policy (PII tagging, retention windows).
