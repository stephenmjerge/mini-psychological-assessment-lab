# 🧪 Mini Psychological Assessment Lab

> **Ethics banner:** This toolkit is for transparent, educational measurement prototyping. Never deploy clinical decisions without licensed oversight, informed consent, and IRB-approved protocols.

Mini Psychological Assessment Lab (PSYLAB) is a YAML-driven scoring engine plus Typer CLI that helps Clinical Science PhD applicants showcase measurement literacy, ethics, and reproducible tooling.

## Features

- YAML specs for each instrument (PHQ-9 and GAD-7 to start) with response scales, scoring, and public severity cut-offs.
- `psylab` Typer CLI for listing instruments, scoring CSVs, summarizing results, and generating longitudinal plots.
- Pandas-powered scoring engine with Rich-formatted summaries.
- Example datasets and pytest suite to keep everything reproducible.

## Quick start

```shell
pip install -e .
pytest -q
psylab instruments
psylab score-csv phq9 examples/sample_phq9.csv > out.csv
psylab summary "PHQ-9" out.csv
psylab plot "PHQ-9" examples/sample_panel_long.csv --save phq9_progress.png
```

## Repository layout

```
psylab/
  instruments/          # YAML specs
  cli.py                # Typer entry point (`psylab`)
  scoring.py            # Dataframe-friendly scoring helpers
  plotting.py           # Longitudinal matplotlib helper
examples/               # Sample CSVs for demos/tests
README.md               # Ethics banner + onboarding
pyproject.toml          # Editable install + Typer script
```

## What to do next (fastest admissions ROI)

1. Add two more YAML specs today (`pcl5.yaml`, `bdi2.yaml`) mirroring the PHQ-9/GAD-7 pattern.
2. Commit & document: keep the ethics banner up top, then capture a 60-sec GIF demo of the CLI.
3. Open issues labeled `good first issue` to invite focused PRs (teamwork signal).
4. Wire up GitHub Actions so `pytest -q` runs on every pull request.
5. Pin a short README rationale on why YAML-driven scoring improves transparency and teaching.

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
