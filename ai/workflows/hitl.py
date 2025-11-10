"""Human-in-the-loop workflow stubs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HitlEscalation:
    tenant: str
    request_id: str
    reason: str
    channel: str = "#atlas-hitl"

    def to_payload(self) -> dict[str, str]:
        return {
            "tenant": self.tenant,
            "request_id": self.request_id,
            "reason": self.reason,
            "channel": self.channel,
            "timestamp": datetime.utcnow().isoformat(),
        }


def route_to_human(escalation: HitlEscalation) -> None:
    payload = escalation.to_payload()
    # TODO: push to Slack webhook / n8n flow
    print(f"[HITL] send to {payload['channel']} :: {payload}")
