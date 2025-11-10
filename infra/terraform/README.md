# Terraform Scaffold

This directory holds a thin wrapper around the Atlas infrastructure:
- `modules/network` — VPC/subnet templates.
- `modules/ai-services` — ECS Fargate deployment for the LangGraph orchestrator.
- `modules/observability` — OTLP collector (ECS) + optional Amazon Managed Prometheus workspace.

## Usage
```bash
cd infra/terraform
terraform init
terraform plan -var core_api_url=https://api.example.com -var grafana_workspace=ws-123 -var otlp_endpoint=https://otel.example.com
```

These modules are intentionally incomplete but show reviewers how you manage IaC for multi-tenant AI workloads. Flesh them out with subnets, ALBs, IAM, etc., as you implement the platform. To enable the observability module, pass VPC subnet + security group IDs so the collector can accept traffic from core services.
