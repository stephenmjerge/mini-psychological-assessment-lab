# 🧪 Mini Psychological Assessment Lab

> **Ethics banner (research use only):** MPAL is a measurement prototyping sandbox. Do not use it for diagnosis or treatment decisions unless the workflow is validated, cleared by your IRB, and operated under licensed clinical supervision with informed consent and HIPAA-compliant safeguards.

Mini Psychological Assessment Lab (MPAL) is a YAML-driven scoring engine and Typer CLI for defining, scoring, and reviewing psychological assessment instruments. It is currently maintained by a single researcher and published publicly for transparency.

## Capabilities

- Load PHQ-9, GAD-7, PCL-5, and BDI-II specs straight from YAML (field names, scoring ranges, severity cutoffs).
- Score wide-format CSVs and emit severity labels plus respondent metadata.
- Summarize scored output with counts, descriptive stats, and severity distribution tables.
- Plot longitudinal panels (`psylab plot`) for progress reviews using Matplotlib.
- Ship examples, tests, and GitHub Actions so every change can be demonstrated and validated quickly.

![MPAL CLI demo placeholder](docs/psylab-demo.gif)  
_Replace this placeholder GIF with a 60-second capture of your actual CLI session for reviewers._

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

MPAL targets Python 3.9+ and uses pandas, Typer, Rich, Matplotlib, and PyYAML.

## CLI cheatsheet

| Command | Purpose | Example |
| --- | --- | --- |
| `psylab instruments` | List bundled instruments and metadata | `psylab instruments` |
| `psylab score-csv <instrument> <responses.csv> [-o out.csv]` | Score a wide CSV | `psylab score-csv phq9 examples/sample_phq9.csv -o phq9_scores.csv` |
| `psylab summary <instrument> <scored.csv>` | Summaries & severity counts | `psylab summary "PHQ-9" phq9_scores.csv` |
| `psylab plot "<Instrument Name>" <panel.csv> --save plot.png` | Plot longitudinal scores | `psylab plot "PHQ-9" examples/sample_panel_long.csv --save phq9_progress.png` |

Run `psylab --help` or append `--help` to any subcommand for option details.

## Data requirements

- **score-csv** expects a wide CSV where column names match the YAML `field` entries (`q1`, `q2`, …) plus an optional `participant_id`.
- **summary** expects the CSV produced by `score-csv`.
- **plot** expects tidy/long data with `participant_id`, `instrument`, `date`, and `score` columns (see `examples/sample_panel_long.csv`).

Sample files live in `examples/` so you can validate the workflow end-to-end.

## Instrument specs

YAML files live in `psylab/instruments/`. Each file defines:

```yaml
instrument:  # ids, labels, domains, citations
items:       # mapping of item ids to CSV field names & prompts
scoring:     # response scale metadata, total score recipe, severity bands
```

Adding a new instrument is as simple as dropping in another YAML file that follows this pattern—no Python changes required unless you need custom scoring logic.

## Example session

```bash
psylab instruments
psylab score-csv phq9 examples/sample_phq9.csv -o phq9_scores.csv
psylab summary "PHQ-9" phq9_scores.csv
psylab plot "PHQ-9" examples/sample_panel_long.csv --save demo.png
open demo.png  # or your platform equivalent
```

Swap in your own CSV exports (ensure headers align with the YAML spec) to score real pilot data under supervised research protocols.

## Development workflow

```bash
pip install -e .[dev]
pytest -q
```

Tests cover scoring logic, severity thresholds, CLI commands, and YAML validation. CI (`.github/workflows/ci.yml`) runs pytest on Python 3.9 and 3.11 for pushes and PRs.

## Roadmap

1. Replace `docs/psylab-demo.gif` with a real CLI walkthrough recording.
2. Add domain subscores or flag columns to the YAML specs (especially PCL-5) to mirror clinical interpretations.
3. Introduce severity band overlays to `psylab plot` for quicker visual reads.
4. Build an HTML/PDF report generator (WeasyPrint/Jinja) that consumes scored CSV output.
5. Add an end-to-end test that invokes the CLI commands to catch packaging regressions.
