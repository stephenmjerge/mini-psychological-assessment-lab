---
name: Bug report
about: Report a reproducible issue in MPAL’s CLI, FastAPI dashboard, or scoring pipeline.
title: "[BUG] "
labels: ["bug"]
assignees: []
---

## Summary
Describe the defect and how it impacts assessment workflows or demos.

## Reproduction checklist
- [ ] Reproduces on `main`
- [ ] Happens with a clean virtualenv (`pip install -e .[dev]`)
- [ ] Includes relevant instrument YAML + CSV samples

### Steps to reproduce
1. …
2. …

### Sample command / request
```bash
psylab score ... # include full CLI command, HTTP request, or code snippet
```

## Expected vs. actual
- **Expected:** …
- **Actual:** …

## Environment
- OS / version:
- Python version:
- Interface (CLI, FastAPI, notebook):
- Instrument + CSV source:
- Additional env vars or settings:

## Logs / artifacts
Upload stack traces, screenshots, generated tables, or GitHub Actions links.
