# Atlas Demo Script

Use this outline to record screenshots, Loom walkthroughs, or conference-style demos.

## Scenario
Pick one of the variants (Fintech / SaaS Copilot / Platform) and narrate:
1. Persona + pain point.
2. How Atlas modules solve it.
3. Outcome metrics to track.

## Flow Checklist
1. **Login & tenant switcher** (Next.js) — show RBAC, tenant branding, usage caps.
2. **AI workspace** — run a LangGraph agent using contextual data (vector search + data marts).
3. **Workflow automation** — trigger n8n orchestration that routes a human approval.
4. **Observability & cost** — open Grafana dashboard and highlight `COST.md` guardrails.
5. **Deployment story** — point to GitHub Actions run and Terraform plan output.

## Assets To Capture
- Screenshots/GIFs for each step above.
- CLI snippets (dbt run, pytest ai tests, terraform plan).
- Architecture diagram callouts for each persona to reinforce executive storytelling.

## TODO
- Attach sample data bundle + `.env.example` once services are scaffolded.
- Add Loom link once the walkthrough is recorded.
