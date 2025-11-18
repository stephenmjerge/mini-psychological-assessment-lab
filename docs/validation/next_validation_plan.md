# Next Validation Notebook — PCL-5 (Manual vs MPAL)

Purpose: deliver the second validation artifact for the Phase 1 milestone by comparing MPAL’s PCL-5 scoring to a hand-scored reference.

## Scope
- Instrument: PCL-5 (bundled spec already in `psylab/instruments/pcl5.yaml`).
- Data: synthetic respondents with item-level responses + manual totals/severity labels.
- Outputs: parity table (manual vs MPAL totals/severity), severity distribution plot, OSF-exportable notebook.

## Steps
1) Draft sample data
- Create `examples/manual_validation_pcl5.csv` with ~5–10 respondents.
- Columns: `participant_id`, PCL-5 item fields, `manual_total`, `manual_severity`.

2) Notebook scaffold
- Clone the existing PHQ-9/GAD-7 notebook structure.
- Replace instrument ids with `pcl5`; point to the new CSV.
- Include sys.path shim + parity assertions + severity plot.

3) Outputs
- Save notebook to `docs/validation/` (e.g., `mpal_manual_validation_pcl5.ipynb`).
- Export HTML/PDF for OSF and link in README/PortfolioHub once published.

4) OSF publishing
- Upload alongside the existing MPAL validation component (https://osf.io/9fdhq/) with a new sub-component for PCL-5 (matching the GAD-7/PHQ-9 pattern at https://osf.io/82wpk/).

5) Definition of Done
- Passing parity checks (manual_total == MPAL total; severity labels match) for all sample rows.
- Notebook + HTML exported and linked in README/PortfolioHub/LAUNCHPAD.
