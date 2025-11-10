"""Run the LangGraph orchestrator locally to show the end-to-end story."""

from ai.agents.orchestrator import simulate
from ai.workflows.hitl import HitlEscalation, route_to_human


if __name__ == "__main__":
    question = "What does the AI governance workflow look like?"
    state = simulate(question, tenant="demo")
    print("Agent response:", state)
    if state.get("route") == "hitl":
        route_to_human(
            HitlEscalation(
                tenant=state.get("tenant", "demo"),
                request_id="req-001",
                reason="Needs SME approval",
            )
        )
