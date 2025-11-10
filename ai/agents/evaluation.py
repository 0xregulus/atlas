"""Lightweight evaluation harness for LangGraph responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class EvaluationResult:
    sentiment: Literal["positive", "neutral", "negative"]
    hallucination_risk: float
    needs_review: bool


def evaluate_response(question: str, response: str) -> EvaluationResult:
    lower = response.lower()
    hallucination_risk = 0.1
    if "cannot" in lower or "unsure" in lower:
        hallucination_risk = 0.6
    if "unverified" in lower:
        hallucination_risk = 0.8

    needs_review = hallucination_risk >= 0.5 or len(response) < 40
    sentiment: Literal["positive", "neutral", "negative"] = "positive"
    if "sorry" in lower or needs_review:
        sentiment = "negative"

    return EvaluationResult(
        sentiment=sentiment,
        hallucination_risk=round(hallucination_risk, 2),
        needs_review=needs_review,
    )
