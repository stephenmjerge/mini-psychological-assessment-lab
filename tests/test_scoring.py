import math

import pandas as pd
import pytest

from psylab.scoring import ScoringError, score_responses, summarize_scores
from psylab.specs import load_instrument_spec


def test_phq9_scoring_totals():
    spec = load_instrument_spec("phq9")
    df = pd.DataFrame(
        [
            {"participant_id": "1001", "q1": 0, "q2": 1, "q3": 1, "q4": 1, "q5": 0, "q6": 1, "q7": 1, "q8": 0, "q9": 0},
            {"participant_id": "1002", "q1": 2, "q2": 2, "q3": 3, "q4": 2, "q5": 1, "q6": 2, "q7": 2, "q8": 1, "q9": 0},
        ]
    )

    scored = score_responses(spec, df)
    assert scored["total_score"].tolist() == [5.0, 15.0]
    assert scored["severity"].tolist() == ["Mild", "Moderately Severe"]


def test_summary_stats_counts():
    spec = load_instrument_spec("gad7")
    df = pd.DataFrame(
        [
            {"participant_id": "1001", "q1": 0, "q2": 1, "q3": 1, "q4": 1, "q5": 0, "q6": 1, "q7": 1},
            {"participant_id": "1002", "q1": 2, "q2": 2, "q3": 2, "q4": 2, "q5": 2, "q6": 2, "q7": 2},
        ]
    )

    scored = score_responses(spec, df)
    summary = summarize_scores(spec, scored)
    assert summary["n"] == 2
    assert summary["n_scored"] == 2
    assert summary["severity_counts"]["Mild"] == 1
    assert summary["severity_counts"]["Moderate"] == 1


def test_bdi2_scoring_and_severity():
    spec = load_instrument_spec("bdi2")
    low_row = {f"q{i}": 0 for i in range(1, 22)}
    high_row = {f"q{i}": 3 for i in range(1, 22)}
    df = pd.DataFrame([low_row, high_row])

    scored = score_responses(spec, df)
    assert scored["total_score"].tolist() == [0.0, 63.0]
    assert scored["severity"].tolist() == ["Minimal", "Severe"]


def test_pcl5_missing_columns_raise():
    spec = load_instrument_spec("pcl5")
    df = pd.DataFrame([{"q1": 1, "q2": 2}])  # missing q3..q20

    with pytest.raises(ScoringError):
        score_responses(spec, df)


def test_pcl5_severity_thresholds():
    spec = load_instrument_spec("pcl5")
    moderate = {f"q{i}": 1 for i in range(1, 21)}  # total 20 -> Subthreshold
    high = {f"q{i}": 4 for i in range(1, 21)}  # total 80 -> Probable PTSD
    df = pd.DataFrame([moderate, high])

    scored = score_responses(spec, df)
    assert scored["severity"].tolist() == ["Subthreshold", "Probable PTSD"]


def test_gad7_scoring_respects_severity_thresholds():
    spec = load_instrument_spec("gad7")
    minimal = {"participant_id": "1001", "q1": 1, "q2": 0, "q3": 1, "q4": 0, "q5": 1, "q6": 0, "q7": 1}
    moderate = {"participant_id": "1002", "q1": 2, "q2": 2, "q3": 2, "q4": 2, "q5": 2, "q6": 1, "q7": 1}
    df = pd.DataFrame([minimal, moderate])

    scored = score_responses(spec, df)
    assert scored["total_score"].tolist() == [4.0, 12.0]
    assert scored["severity"].tolist() == ["Minimal", "Moderate"]


def test_gad7_missing_responses_yield_nan_total():
    spec = load_instrument_spec("gad7")
    df = pd.DataFrame([
        {"participant_id": "1003", "q1": 1, "q2": 1, "q3": None, "q4": 1, "q5": 0, "q6": 0, "q7": 0}
    ])

    scored = score_responses(spec, df)
    assert math.isnan(scored.loc[0, "total_score"])
    assert scored.loc[0, "severity"] is None


def test_gad7_non_numeric_entry_raises():
    spec = load_instrument_spec("gad7")
    df = pd.DataFrame([
        {"participant_id": "1004", "q1": 1, "q2": 1, "q3": "bad", "q4": 1, "q5": 1, "q6": 1, "q7": 1}
    ])

    with pytest.raises(ScoringError):
        score_responses(spec, df)
