import pandas as pd

from psylab.scoring import score_responses, summarize_scores
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
    assert summary["severity_counts"]["Severe"] == 1
