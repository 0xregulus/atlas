# Playbooks

## Incident Escalation (AI/HITL)
1. LangGraph flags `route=hitl` or Slack `/webhooks/stripe` anomaly events.
2. n8n flow `workflows/hitl-escalation.md` posts to `#atlas-hitl` with context (tenant, tokens, cost).
3. On-call acknowledges in Slack, updates the incident doc, and (if needed) triggers `/metrics/usage` summary via Postman to assess blast radius.
4. Close the loop by recording learnings in `docs/product/runbook.md` and updating guardrails.

## Cost Anomaly Response
1. Alert from Grafana panel (tokens vs plan) posts to `#atlas-cost` via n8n webhook.
2. Run the `Record Usage Event` Postman request with `source=investigation` to log manual adjustments.
3. Coordinate with finance/billing to update Stripe plans, then re-run `GET /billing/{tenant}/preview` to confirm the fix.

## On-Call Tips
- Keep `CORE_API_BEARER_TOKEN` handy (generate via `/auth/token`).
- Use the Observability Panel embed on the dashboard for live traces.
- Reference `automation/workflows/n8n-hitl.yml` for detailed flow settings.
