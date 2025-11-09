from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import typer
from rich.console import Console
from rich.table import Table

from .plotting import plot_panel
from .scoring import ScoringError, score_responses, summarize_scores
from .specs import list_instruments, load_instrument_spec

app = typer.Typer(help="Mini Psychological Assessment Lab CLI")
console = Console()


@app.command()
def instruments() -> None:
    """List bundled instruments."""
    rows = list_instruments()
    if not rows:
        console.print("[yellow]No instruments are bundled yet.[/yellow]")
        raise typer.Exit(code=1)

    table = Table("ID", "Name", "Version", "Description")
    for row in rows:
        table.add_row(row.get("id", ""), row.get("name", ""), row.get("version", ""), row.get("description", ""))
    console.print(table)


@app.command("score-csv")
def score_csv(
    instrument: str = typer.Argument(..., help="Instrument id or name"),
    csv_path: Path = typer.Argument(..., exists=True, readable=True),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Write output CSV to a file"),
    respondent_id: Optional[str] = typer.Option("participant_id", help="Column holding respondent ids"),
) -> None:
    """Score a wide CSV of responses."""

    spec = load_instrument_spec(instrument)
    data = pd.read_csv(csv_path)
    try:
        scored = score_responses(spec, data, respondent_id_col=respondent_id)
    except ScoringError as exc:
        console.print(f"[red]Scoring failed:[/red] {exc}")
        raise typer.Exit(code=1)

    if out:
        scored.to_csv(out, index=False)
        console.print(f"[green]Saved scores to {out}[/green]")
    else:
        console.print(scored.to_csv(index=False))


@app.command()
def summary(
    instrument: str = typer.Argument(..., help="Instrument id or name"),
    scored_csv: Path = typer.Argument(..., exists=True, readable=True),
) -> None:
    """Summarize scored output."""

    spec = load_instrument_spec(instrument)
    data = pd.read_csv(scored_csv)
    try:
        stats = summarize_scores(spec, data)
    except ScoringError as exc:
        console.print(f"[red]Summary failed:[/red] {exc}")
        raise typer.Exit(code=1)

    table = Table(title=f"{stats['instrument']} summary")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("n", str(stats["n"]))
    table.add_row("n_scored", str(stats["n_scored"]))
    for label in ("mean", "std", "min", "max"):
        value = stats.get(label)
        table.add_row(label, f"{value:.2f}" if value is not None else "-")

    if stats.get("severity_counts"):
        for severity, count in stats["severity_counts"].items():
            table.add_row(f"severity:{severity}", str(count))

    console.print(table)


@app.command()
def plot(
    instrument: str = typer.Argument(..., help="Instrument display name, e.g. 'PHQ-9'"),
    panel_csv: Path = typer.Argument(..., exists=True, readable=True),
    save: Path = typer.Option(Path("progress.png"), "--save", help="File to save plot"),
) -> None:
    """Plot longitudinal scores from a tidy/long CSV."""

    data = pd.read_csv(panel_csv)
    required = {"participant_id", "instrument", "date", "score"}
    if missing := required - set(data.columns):
        console.print(f"[red]panel CSV missing required columns: {', '.join(sorted(missing))}[/red]")
        raise typer.Exit(code=1)

    output = plot_panel(data, instrument_name=instrument, save_path=save)
    console.print(f"[green]Saved plot to {output}[/green]")
