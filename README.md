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
| `psylab instruments [--json]` | List bundled instruments (optionally JSON for scripting) | `psylab instruments --json` |
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

### Instrument families and roadmap targets

MPAL currently ships depression (PHQ-9, BDI-II), anxiety (GAD-7), and PTSD/trauma (PCL-5) measures. The broader clinical landscape that clinical psychology trainees work with can be grouped as follows:

| Family | Example instruments |
| --- | --- |
| Depression | PHQ-9, BDI-II, CES-D, HAM-D, MADRS |
| Anxiety | GAD-7, BAI, HAM-A, SCARED |
| PTSD / Trauma | PCL-5, ACE, CAPS-5, IES-R, TSQ |
| Substance use | AUDIT, DAST-10, CAGE/CAGE-AID, ASSIST |
| Suicidality & risk | C-SSRS, SAFE-T, SBQ-R |
| ADHD | ASRS, Conners, WURS |
| Personality | MMPI-3, PAI, MCMI-IV, Rorschach, TAT |
| Cognitive / neuropsych | WAIS-IV, WISC-V, RBANS, MoCA, MMSE |
| Mood / bipolar | MDQ, YMRS, CARS-M |
| Eating disorders | EDE-Q, EAT-26, SCOFF |
| OCD | Y-BOCS, OCI-R |
| Autism spectrum | ADOS-2, ADI-R, SRS-2 |
| Relationship / attachment | ECR-R, AAI, Dyadic Adjustment Scale |
| Somatic symptoms | PHQ-15, SOMS |
| General distress | K10/K6, OQ-45, CORE-10/CORE-OM |
| Functioning / disability | WHODAS 2.0, GAF, SDS |
| Child & adolescent behavior | CBCL, BASC-3, Vanderbilt ADHD rating |
| Specialized clinical | PQ-B, HCL-32, PSQI, DERS |

This taxonomy doubles as the long-term feature backlog: every time a YAML spec is added for a new family, MPAL becomes a more complete lab for organizing, scoring, interpreting, and tracking change across the full battery clinical training programs expect.

## Example session

```bash
psylab instruments
psylab score-csv phq9 examples/sample_phq9.csv -o phq9_scores.csv
psylab summary "PHQ-9" phq9_scores.csv
psylab plot "PHQ-9" examples/sample_panel_long.csv --save demo.png
open demo.png  # or your platform equivalent
```

Swap in your own CSV exports (ensure headers align with the YAML spec) to score real pilot data under supervised research protocols.

## Web dashboard

Prefer a point-and-click workflow? Launch the bundled FastAPI dashboard:

```bash
psylab gui --host 127.0.0.1 --port 8000
```

Then open the printed URL in your browser to:

- Browse bundled instruments.
- Upload a wide CSV and view scored output as a table + raw CSV text.
- Upload scored CSVs to view summaries and severity counts.
- Upload longitudinal CSVs to render Matplotlib progress plots directly in the page.

The GUI is local-only by default; pass `--host 0.0.0.0` if you need other devices on your network to reach it.

## Development workflow

```bash
pip install -e .[dev]
pytest -q
```

Tests cover scoring logic, severity thresholds, CLI commands, and YAML validation. CI (`.github/workflows/ci.yml`) runs pytest on Python 3.9 and 3.11 for pushes and PRs.

## Roadmap

1. Replace `docs/psylab-demo.gif` with a real CLI walkthrough recording.
2. Add domain subscores or flag columns to the YAML specs (especially PCL-5) to mirror clinical interpretations.
3. Expand YAML coverage using the family taxonomy above (e.g., add CES-D, GAD-7 child variants, ACE, AUDIT, C-SSRS) so each major diagnostic cluster has at least one exemplar.
4. Introduce severity band overlays and reference lines to `psylab plot` for quicker visual reads.
5. Build an HTML/PDF report generator (WeasyPrint/Jinja) that consumes scored CSV output.
6. Add an end-to-end test that invokes the CLI commands to catch packaging regressions.
