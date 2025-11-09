# 🧪 Mini Psychological Assessment Lab

> **Ethics banner:** This toolkit is for transparent, educational measurement prototyping. Never deploy clinical decisions without licensed oversight, informed consent, and IRB-approved protocols.

Mini Psychological Assessment Lab (MPAL) is a YAML-driven scoring engine and Typer CLI for defining, scoring, and reviewing psychological assessment instruments.

## Features

- YAML specs for each instrument (PHQ-9, GAD-7, PCL-5, and BDI-II) with response scales, scoring, and public severity cut-offs.
- `psylab` Typer CLI for listing instruments, scoring CSVs, summarizing results, and generating longitudinal plots.
- Pandas-powered scoring engine with Rich-formatted summaries.
- Example datasets and pytest suite to keep everything reproducible.

## Quick start

```shell
pip install -e .[dev]  # editable install + pytest extras
pytest -q
psylab instruments
psylab score-csv phq9 examples/sample_phq9.csv > out.csv
psylab summary "PHQ-9" out.csv
psylab plot "PHQ-9" examples/sample_panel_long.csv --save phq9_progress.png
```

![PSYLAB CLI demo](docs/psylab-demo.gif)

_(Replace the placeholder GIF with a 60-sec capture of the CLI workflow to give reviewers instant context.)_

## Repository layout

```
psylab/
  instruments/          # YAML specs (PHQ-9, GAD-7, PCL-5, BDI-II)
  cli.py                # Typer entry point (`psylab`)
  scoring.py            # Dataframe-friendly scoring helpers
  plotting.py           # Longitudinal matplotlib helper
examples/               # Sample CSVs for demos/tests
docs/psylab-demo.gif    # Drop-in CLI walkthrough GIF (replace placeholder)
.github/workflows/ci.yml# Pytest-on-PR GitHub Actions workflow
README.md               # Ethics banner + onboarding
pyproject.toml          # Editable install + Typer script
```

## Why YAML-driven scoring?

1. **Transparent logic:** Committees can audit the exact scoring recipe in `psylab/instruments/*.yaml` instead of reading opaque code.
2. **Teachable specs:** Adding instruments is a matter of structured metadata, so collaborators can learn by editing YAML, not Python.
3. **Reproducible reviews:** YAML diffs show when cutoffs, prompts, or scoring logic change—critical for ethics reviews and IRB appendices.

## What to do next (fastest admissions ROI)

1. Swap the placeholder demo GIF with a real CLI walkthrough (use `asciinema` + `agg` or `ttystudio` → `gif`).
2. Open the suggested GitHub issues below (`good first issue` label) to invite scoped community help.
3. Expand severity guidance: include domain subscores or flagging logic per instrument.
4. Bundle a simple HTML/PDF report generator for committee-ready appendices.
5. Publish the repo and tag `v0.1.0` once CI is green.

## Suggested “good first issues”

| Label | Pitch | Rationale |
| --- | --- | --- |
| good first issue | Add domain subscores for PCL-5 YAML | Demonstrates psychometrics thinking without touching Python. |
| good first issue | Improve plotting CLI with severity bands | Practically shows data viz chops. |
| good first issue | Build HTML report exporter | Highlights communication + templating skills. |
| good first issue | Add integration test that round-trips CLI commands | Signals commitment to reproducibility. |

## Instrument YAML anatomy

Each YAML describes:

- `instrument`: id, name, citation, description, domains.
- `items`: field names expected in the response CSV.
- `scoring`: response scale metadata, the total score recipe, and severity thresholds.

Because specs live in version control, reviewers can trace exactly how scores are computed.

## Example workflow

1. Field responses in any REDCap/REDCap-like tool.
2. Export a CSV with columns that match the YAML `field` names.
3. Run `psylab score-csv <instrument> responses.csv -o scores.csv`.
4. Share `psylab summary` output with your lab mentor, plus a `psylab plot` PNG in your SOP appendix.

## Testing

Run `pytest -q` to validate scoring logic, CLI wiring, and YAML coverage.
