from __future__ import annotations

import math
from typing import Any, Dict, Optional

import pandas as pd


class ScoringError(Exception):
    """Raised when required columns or responses are missing."""


def _coerce_numeric(value: Any) -> Optional[float]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ScoringError(f"Cannot convert response '{value}' to a number") from exc
    if math.isnan(numeric):
        return None
    return numeric


def _severity_label(score: float, spec: Dict[str, Any]) -> Optional[str]:
    interpretation = (spec.get("scoring") or {}).get("interpretation") or {}
    for band in interpretation.get("severity_thresholds", []):
        lower = band.get("min", float("-inf"))
        upper = band.get("max", float("inf"))
        if lower <= score <= upper:
            return band.get("label")
    return None


def score_responses(
    spec: Dict[str, Any],
    responses: pd.DataFrame,
    *,
    respondent_id_col: Optional[str] = "participant_id",
) -> pd.DataFrame:
    """Return scored totals for the provided responses."""

    scoring_cfg = (spec.get("scoring") or {}).get("total")
    if not scoring_cfg:
        raise ScoringError("Spec is missing a scoring.total definition")

    items_section = {item["id"]: item for item in spec.get("items", [])}
    item_ids = scoring_cfg.get("items") or []
    missing_items = [item_id for item_id in item_ids if item_id not in items_section]
    if missing_items:
        raise ScoringError(f"Spec references unknown items: {', '.join(missing_items)}")

    required_columns = [items_section[item_id]["field"] for item_id in item_ids]
    missing_columns = [col for col in required_columns if col not in responses.columns]
    if missing_columns:
        raise ScoringError(
            "Input data is missing required columns: " + ", ".join(missing_columns)
        )

    scored_rows = []
    for _, row in responses.iterrows():
        record: Dict[str, Any] = {
            "instrument_id": spec["instrument"]["id"],
            "instrument_name": spec["instrument"].get("name"),
        }
        if respondent_id_col and respondent_id_col in responses.columns:
            record["respondent_id"] = row.get(respondent_id_col)

        scores = []
        for item_id in item_ids:
            field_name = items_section[item_id]["field"]
            scores.append(_coerce_numeric(row.get(field_name)))

        if any(val is None for val in scores):
            record["total_score"] = math.nan
            record["severity"] = None
        else:
            total = float(sum(scores))
            record["total_score"] = total
            record["severity"] = _severity_label(total, spec)

        scored_rows.append(record)

    return pd.DataFrame(scored_rows)


def summarize_scores(spec: Dict[str, Any], scored: pd.DataFrame) -> Dict[str, Any]:
    if "total_score" not in scored.columns:
        raise ScoringError("Scored data must include a total_score column")

    total_series = scored["total_score"].dropna()
    severity_series = scored.get("severity")

    summary = {
        "instrument": spec["instrument"].get("name"),
        "n": len(scored),
        "n_scored": int(total_series.count()),
        "mean": float(total_series.mean()) if not total_series.empty else None,
        "std": float(total_series.std(ddof=0)) if len(total_series) > 1 else None,
        "min": float(total_series.min()) if not total_series.empty else None,
        "max": float(total_series.max()) if not total_series.empty else None,
        "severity_counts": {},
    }

    if severity_series is not None:
        counts = severity_series.dropna().value_counts().to_dict()
        summary["severity_counts"] = counts

    return summary
