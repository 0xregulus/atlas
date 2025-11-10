# Automation & Ops Playbooks

Holds CI/CD workflows, operational runbooks, and n8n recipes.

## Subdirectories
- `ci/` — shared scripts for lint/test packages.
- `workflows/` — reusable GitHub/n8n workflow specs.
- `playbooks/` — incident response, release, and escalation checklists (see `playbooks/README.md` for HITL and cost anomaly flows).

## Next Tasks
- Extend GitHub Actions beyond lint/test/build (e.g., Docker image publish, deploy gates).
- Add n8n flows for human approvals and cost anomaly responses.
- Document on-call rotations and escalation contacts.
