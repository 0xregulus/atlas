from ai.agents.orchestrator import simulate
from ai.vector_search.cache import cache


def test_simulate_returns_evaluation():
    cache.clear()
    state = simulate("How do I approve human escalations?", tenant="demo")
    assert state["route"] in {"auto", "hitl"}
    assert "evaluation" in state
    evaluation = state["evaluation"]
    assert "hallucination_risk" in evaluation


def test_semantic_cache_short_circuits():
    cache.clear()
    first = simulate("What is the governance workflow?", tenant="demo")
    assert first.get("cached") in {False, None}
    second = simulate("What is the governance workflow?", tenant="demo")
    assert second.get("cached") is True
