# Clinician Quickstart

Minimal copy/paste steps to score and review assessments without digging into code.

## 1) Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install https://github.com/stephenmjerge/mini-psychological-assessment-lab/releases/latest/download/mpal-0.1.1-py3-none-any.whl
```

## 2) Fastest first run
```bash
psylab demo
```
Outputs land in `outputs/demo_*` with scores CSV, summary JSON, and an HTML report.

## 3) Score your CSV
```bash
psylab score-csv phq9 your_responses.csv --out scores.csv --html-report
psylab summary phq9 scores.csv
```

## 4) Troubleshooting
- Headless/locked-down machines:  
  `export MPAL_DISABLE_PLOTS=1`  
  `export MPLCONFIGDIR=$PWD/.cache/mpl`  
  `export XDG_CACHE_HOME=$PWD/.cache/xdg`
- Validate without writing outputs: add `--dry-run` to `score-csv`.
- Environment check: `psylab doctor` (Python, deps, optional input path).
- Missing columns: ensure your CSV headers match the instrument YAML fields (see `psylab instruments --json` for field names).

## 5) Share safely
Send only outputs (`scores.csv`, `summary.json`, `report.html`). Include the command you ran and the MPAL version.
