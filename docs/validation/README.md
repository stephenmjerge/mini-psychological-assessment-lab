# MPAL Manual Validation Artifacts

This directory stores notebooks and helper files that compare MPAL-generated scores against manual scoring references.

Current contents:

- `mpal_manual_validation.ipynb` — Loads the PHQ-9 and GAD-7 reference CSVs from `examples/`, runs them through `psylab.score_responses`, and confirms that MPAL’s totals and severity bands match the hand-scored ground truth. The notebook also visualizes severity distributions (manual vs MPAL) for each instrument.

The paired CSVs (`examples/manual_validation_phq9.csv` and `examples/manual_validation_gad7.csv`) include synthetic item responses plus `manual_total`/`manual_severity` columns. They exist purely for validation and contain no sensitive data.
