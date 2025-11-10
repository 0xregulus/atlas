"""CLI entrypoint for Atlas AI services."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich import print_json

from .agents.orchestrator import simulate
from .config import get_settings

app = typer.Typer(help="Run LangGraph simulations and inspections")


@app.command()
def run(
    question: str = typer.Argument(..., help="User question for the agent"),
    tenant: str | None = typer.Option(None, help="Tenant id to scope the run"),
    dump_file: Path | None = typer.Option(None, help="Optional path to store raw output"),
) -> None:
    """Execute the LangGraph pipeline and print the final state."""
    typer.echo("Running LangGraph simulation...", err=True)
    state = simulate(question, tenant)
    print_json(data=state)
    if dump_file:
        dump_file.write_text(json.dumps(state, indent=2))
        typer.echo(f"Saved output to {dump_file}")


@app.command()
def settings() -> None:
    """Show the resolved AI service settings."""
    print_json(data=get_settings().model_dump())


if __name__ == "__main__":
    app()
