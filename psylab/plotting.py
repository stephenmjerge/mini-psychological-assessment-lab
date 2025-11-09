from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def plot_panel(
    data: pd.DataFrame,
    *,
    instrument_name: str,
    save_path: Optional[Path] = None,
) -> Path:
    subset = data[data["instrument"].str.lower() == instrument_name.lower()].copy()
    if subset.empty:
        raise ValueError(f"No rows found for instrument '{instrument_name}'")

    subset["date"] = pd.to_datetime(subset["date"])

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for respondent, group in subset.sort_values("date").groupby("participant_id"):
        ax.plot(
            group["date"],
            group["score"],
            marker="o",
            label=str(respondent),
        )

    ax.set_title(f"{instrument_name} progress")
    ax.set_ylabel("Score")
    ax.set_xlabel("Date")
    ax.margins(x=0.05, y=0.1)
    ax.legend(title="Participant", loc="upper right", fontsize="small")
    ax.grid(True, alpha=0.3)

    output = Path(save_path) if save_path else Path("plot.png")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output
