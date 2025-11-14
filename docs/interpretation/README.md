# MPAL Scoring Interpretation Sheet (Research Use Only)

Use this single page when presenting MPAL outputs to supervisors, admissions
committees, or lab collaborators. All severity labels mirror public scoring
instructions; MPAL is for research/educational workflows only.

## Instruments & Severity Bands

| Instrument | Score Range | Severity Labels | Citation |
| --- | --- | --- | --- |
| **PHQ-9** | 0–27 | Minimal (0–4), Mild (5–9), Moderate (10–14), Moderately Severe (15–19), Severe (20–27) | Kroenke et al. (2001) |
| **GAD-7** | 0–21 | Minimal (0–4), Mild (5–9), Moderate (10–14), Severe (15–21) | Spitzer et al. (2006) |
| **PCL-5** | 0–80 | Below threshold (<31), Subthreshold (31–37), Probable PTSD (≥38) | Blevins et al. (2015) |
| **BDI-II** | 0–63 | Minimal (0–13), Mild (14–19), Moderate (20–28), Severe (29–63) | Beck et al. (1996) |

*See `psylab/instruments/*.yaml` for the exact severity thresholds used by the
CLI/SDK.*

## Usage checklist
- Include the instrument name, total score, and severity label in your reports.
- Note the date of administration and whether items were missing (MPAL outputs `NaN` if responses are incomplete).
- Reference the instrument citation when sharing results externally (see table above).
- Add contextual language: "research-use only" / "not a clinical diagnosis".

## Integrating with plots & reports
- Combine this sheet with `docs/assets/gad7_trend_demo.png` to show severity shifts over time.
- Highlight key thresholds in your dashboards (e.g., shading severity bands in Matplotlib plots).
- When drafting manuscripts or mini-reviews, link back to `docs/mini-review.md` for literature context.

## Next steps
- Extend the table as new instruments are added (CES-D, ACE, AUDIT, etc.).
- Convert this README into a printable PDF (WeasyPrint/Jinja templates) when report generator lands.
