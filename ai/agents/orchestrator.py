"""LangGraph orchestrator with semantic cache + evaluation hooks."""

from __future__ import annotations

from dataclasses import asdict
from typing import Literal, TypedDict

from langgraph.graph import StateGraph
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from ..config import get_settings
from ..vector_search.client import VectorClient
from ..vector_search.cache import cache as semantic_cache
from ..services.core_client import get_catalog, report_usage_event
from .evaluation import evaluate_response, EvaluationResult

settings = get_settings()
if settings.otlp_endpoint:
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otlp_endpoint)))
    trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


class AgentState(TypedDict, total=False):
    question: str
    tenant: str
    context: str
    response: str
    cached: bool
    evaluation: dict
    route: Literal["auto", "hitl"]


def retrieve_context(state: AgentState) -> AgentState:
    client = VectorClient()
    tenant = state.get("tenant") or settings.default_tenant
    docs = client.similarity_search(
        tenant=tenant,
        query=state["question"],
        collection=settings.vector_collection,
    )
    catalog = get_catalog(tenant)
    if catalog:
        docs.extend(
            {"id": f"catalog-{item['name']}", "content": f"Dataset {item['name']}: {item['description']}"} for item in catalog
        )
    context = "\n".join(doc["content"] for doc in docs)
    return {"context": context, "tenant": tenant}


def call_llm(state: AgentState) -> AgentState:
    tenant = state.get("tenant") or settings.default_tenant
    question = state.get("question", "")
    context = state.get("context", "")

    if settings.enable_semantic_cache:
        cached_entry = semantic_cache.get(tenant, question)
        if cached_entry:
            return {
                "response": cached_entry.response,
                "context": cached_entry.context,
                "cached": True,
            }

    response = f"Based on approved knowledge ({len(context.split())} tokens), here is the answer to '{question}'."
    semantic_cache.set(tenant, question, response=response, context=context)
    return {"response": response, "cached": False}


def evaluate(state: AgentState) -> AgentState:
    result: EvaluationResult = evaluate_response(state.get("question", ""), state.get("response", ""))
    return {"evaluation": asdict(result)}


def decide_handoff(state: AgentState) -> AgentState:
    evaluation = state.get("evaluation")
    needs_review = evaluation.get("needs_review") if evaluation else None
    if needs_review is None:
        response = state.get("response", "")
        needs_review = "cannot" in response.lower() or len(response) < 40
    route: Literal["auto", "hitl"] = "hitl" if needs_review else "auto"
    return {"route": route}


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve_context)
    graph.add_node("llm", call_llm)
    graph.add_node("evaluate", evaluate)
    graph.add_node("decision", decide_handoff)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "llm")
    graph.add_edge("llm", "evaluate")
    graph.add_edge("evaluate", "decision")

    return graph


def simulate(question: str, tenant: str | None = None) -> AgentState:
    graph = build_graph()
    runnable = graph.compile()
    tenant_id = tenant or settings.default_tenant
    final_state = runnable.invoke({"question": question, "tenant": tenant_id})
    tokens = len(final_state.get("context", "").split())
    latency = None
    report_usage_event(tenant_id, tokens=tokens, latency_ms=latency)
    return final_state


if __name__ == "__main__":
    state = simulate("How do I route escalations to humans?")
    print(state)
