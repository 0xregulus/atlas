# n8n Workflow: HITL Escalation

1. Trigger: webhook exposed at `/n8n/hitl` (used by LangGraph HITL route + cost alerts).
2. Fetch tenant usage via `GET {{CORE_API_URL}}/tenants/current` (requires bearer token from `/auth/token`).
3. Post to Slack `#atlas-hitl` with:
   - Tenant + plan tier
   - Token spike / latency info (from `/metrics/usage/daily`)
   - Deep link to dashboard (`NEXT_PUBLIC_OBSERVABILITY_PANEL_URL`).
4. Optional branch → create PagerDuty incident if `usage.plan == 'scale'` and events > threshold.

Store secrets (`CORE_API_BEARER_TOKEN`, Slack webhook) in n8n credentials; reuse this flow for cost anomaly playbook.
