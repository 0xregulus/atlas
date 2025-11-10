# Infrastructure & Observability

IaC plus deployment targets for Atlas.

## Subdirectories
- `terraform/` — networking foundations, shared services, state definitions.
- `cdk/` — application stacks (ECS services, queues, buckets) modeled with higher-level constructs.
- `observability/` — Grafana/Loki/Prometheus manifests, alerting configs.
- `platform/` — reusable modules (VPC, service mesh, secret management).

## Next Tasks
- Create Terraform remote state + workspace strategy ADR.
- Add CDK app that provisions ECS service + Qdrant cluster.
- Wire the observability module (collector + Amazon Managed Prometheus) into staging environments.
- Document observability SLIs/SLOs and integrate with COST guardrails.
- Provide developer bootstrap script for local Docker parity.
