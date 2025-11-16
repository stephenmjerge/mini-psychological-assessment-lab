# Validation Sample Data

The CSV files in this directory provide paired manual scoring references for the MPAL validation notebook.

- `manual_validation_phq9.csv` — Five PHQ-9 respondents (participant ids 2001–2005) with item-level responses, manual totals, and an explicitly logged severity label using the public PHQ-9 cutoffs.
- `manual_validation_gad7.csv` — Five GAD-7 respondents with the same structure as above.

How to use them:

1. Feed each CSV into `psylab.score_responses` to produce MPAL totals/severity labels.
2. Compare the MPAL output to the `manual_total`/`manual_severity` columns to confirm parity.
3. The validation notebook at `docs/validation/mpal_manual_validation.ipynb` automates this comparison and generates a severity distribution plot.

These records are synthetic and exist purely for demonstration and admissions-review artifacts. They do **not** contain PHI/PII beyond the dummy participant ids.
