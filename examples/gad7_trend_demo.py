"""Generate a simple GAD-7 severity trend plot using sample_panel_long.csv."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "examples" / "sample_panel_long.csv"
OUTDIR = BASE / "docs" / "assets"
OUTDIR.mkdir(parents=True, exist_ok=True)

SEVERITY_BANDS = [
    (0, 4, "Minimal", "#e0f7fa"),
    (5, 9, "Mild", "#c5e1a5"),
    (10, 14, "Moderate", "#ffecb3"),
    (15, 21, "Severe", "#ffccbc"),
]


def main() -> None:
    df = pd.read_csv(DATA, parse_dates=["date"])
    gad7 = df[df["instrument"].str.upper() == "GAD-7"].copy()
    if gad7.empty:
        raise SystemExit("No GAD-7 rows found in sample_panel_long.csv")

    fig, ax = plt.subplots(figsize=(6, 4))
    for pid, sub in gad7.groupby("participant_id"):
        sub = sub.sort_values("date")
        ax.plot(sub["date"], sub["score"], marker="o", label=f"Participant {pid}")

    for lower, upper, label, color in SEVERITY_BANDS:
        ax.axhspan(lower - 0.5, upper + 0.5, color=color, alpha=0.25)
        ax.text(gad7["date"].min(), upper, label, fontsize=8, va="bottom", ha="left", alpha=0.5)

    ax.set_title("GAD-7 Severity Trend (Sample Data)")
    ax.set_ylabel("GAD-7 Score")
    ax.set_xlabel("Date")
    ax.set_ylim(0, 21)
    ax.legend(loc="upper right")
    fig.autofmt_xdate()

    output_path = OUTDIR / "gad7_trend_demo.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
