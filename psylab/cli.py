from __future__ import annotations

import json
import sys
from datetime import datetime
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
def instruments(
    json_output: bool = typer.Option(False, "--json", help="Emit instrument metadata as JSON"),
) -> None:
    """List bundled instruments."""
    rows = list_instruments()
    if not rows:
        console.print("[yellow]No instruments are bundled yet.[/yellow]")
        raise typer.Exit(code=1)

    if json_output:
        import json

        typer.echo(json.dumps(rows, indent=2))
        return

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
    html_report: bool = typer.Option(False, "--html-report", help="Write a simple HTML summary alongside CSV output"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate inputs and exit without writing outputs"),
) -> None:
    """Score a wide CSV of responses."""

    spec = load_instrument_spec(instrument)
    data = pd.read_csv(csv_path)
    try:
        scored = score_responses(spec, data, respondent_id_col=respondent_id)
    except ScoringError as exc:
        console.print(f"[red]Scoring failed:[/red] {exc}")
        raise typer.Exit(code=1)

    if dry_run:
        summary = summarize_scores(spec, scored)
        console.print(f"[cyan]Dry run passed for {instrument}[/cyan]")
        console.print(json.dumps(summary, indent=2))
        raise typer.Exit(code=0)

    if out:
        scored.to_csv(out, index=False)
        console.print(f"[green]Saved scores to {out}[/green]")
    else:
        console.print(scored.to_csv(index=False))
        return

    if html_report:
        _write_html_report(scored, spec, out or csv_path.with_name("scores.csv"))


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


def _write_html_report(scored: pd.DataFrame, spec: dict, scores_path: Path, outdir: Path | None = None) -> None:
    outdir = outdir or scores_path.parent
    outdir.mkdir(parents=True, exist_ok=True)
    summary = summarize_scores(spec, scored)
    alerts = []
    if summary.get("n_scored", 0) != summary.get("n", 0):
        alerts.append("Some rows contained missing data and were not scored.")
    html_lines = [
        "<html><head><title>MPAL Report</title></head><body>",
        f"<h1>{summary.get('instrument') or 'Instrument'} Report</h1>",
        f"<p><strong>Rows:</strong> {summary.get('n')}</p>",
        f"<p><strong>Scored:</strong> {summary.get('n_scored')}</p>",
        f"<p><strong>Mean:</strong> {summary.get('mean')}</p>",
        f"<p><strong>Std:</strong> {summary.get('std')}</p>",
        f"<p><strong>Min:</strong> {summary.get('min')}</p>",
        f"<p><strong>Max:</strong> {summary.get('max')}</p>",
        "<h2>Severity counts</h2>",
    ]
    if summary.get("severity_counts"):
        html_lines.append("<ul>")
        for label, count in summary["severity_counts"].items():
            html_lines.append(f"<li>{label}: {count}</li>")
        html_lines.append("</ul>")
    else:
        html_lines.append("<p>No severity labels found.</p>")
    if alerts:
        html_lines.append("<h2>Notes</h2><ul>")
        for note in alerts:
            html_lines.append(f"<li>{note}</li>")
        html_lines.append("</ul>")
    html_lines.append("</body></html>")
    (outdir / "report.html").write_text("\n".join(html_lines), encoding="utf-8")


@app.command()
def demo(outdir: Optional[Path] = typer.Option(None, "--outdir", help="Directory for demo outputs")) -> None:
    """Run a one-command demo using bundled sample data."""
    sample = Path(__file__).resolve().parents[1] / "examples" / "sample_phq9.csv"
    if not outdir:
        stamp = datetime.utcnow().strftime("demo_%Y%m%dT%H%M%SZ")
        outdir = Path("outputs") / stamp
    outdir.mkdir(parents=True, exist_ok=True)
    spec = load_instrument_spec("phq9")
    data = pd.read_csv(sample)
    scored = score_responses(spec, data)
    scores_path = outdir / "scores.csv"
    scored.to_csv(scores_path, index=False)
    summary = summarize_scores(spec, scored)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    _write_html_report(scored, spec, scores_path, outdir=outdir)
    console.print(f"[green]Demo complete[/green] → {outdir}")


@app.command()
def doctor(
    input_csv: Optional[Path] = typer.Option(None, "--input", help="Optional input CSV to check for existence"),
) -> None:
    """Environment sanity checks (Python, deps, key files)."""
    checks = []
    py_ok = sys.version_info >= (3, 9)
    checks.append(("python>=3.9", py_ok, sys.version))
    for mod in ("pandas", "matplotlib", "rich"):
        try:
            module = __import__(mod)
            ver = getattr(module, "__version__", "unknown")
            checks.append((f"{mod} import", True, ver))
        except Exception as exc:  # pragma: no cover - defensive
            checks.append((f"{mod} import", False, str(exc)))
    if input_csv:
        checks.append(("input exists", input_csv.exists(), str(input_csv)))
    passed = True
    for name, ok, note in checks:
        status = "[green]OK[/green]" if ok else "[red]FAIL[/red]"
        console.print(f"{status} {name} ({note})")
        passed = passed and ok
    if not passed:
        raise typer.Exit(code=1)
    console.print("[green]Doctor checks passed.[/green]")


@app.command()
def gui(
    host: str = typer.Option("127.0.0.1", help="Host interface to bind"),
    port: int = typer.Option(8000, help="Port for the web UI"),
) -> None:
    """Launch the MPAL web dashboard."""

    try:
        import uvicorn
    except ImportError as exc:
        console.print("[red]Install the GUI dependencies first: pip install psylab[dev][/red]")
        raise typer.Exit(code=1) from exc

    console.print(f"[cyan]Launching MPAL GUI on http://{host}:{port}[/cyan]")
    uvicorn.run("psylab.webapp:app", host=host, port=port, reload=False)
