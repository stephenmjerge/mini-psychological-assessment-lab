from __future__ import annotations

import base64
import tempfile
from io import StringIO
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from importlib import resources

from .plotting import plot_panel
from .scoring import ScoringError, score_responses, summarize_scores
from .specs import list_instruments, load_instrument_spec

templates = Jinja2Templates(directory=str(resources.files(__package__) / "templates"))
app = FastAPI(title="Mini Psychological Assessment Lab")


def _base_context(request: Request) -> dict:
    return {"request": request, "instruments": list_instruments()}


def _read_csv(upload: UploadFile) -> pd.DataFrame:
    content = upload.file.read()
    if not content:
        raise ValueError("Uploaded file is empty.")
    return pd.read_csv(StringIO(content.decode("utf-8")))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", _base_context(request))


@app.post("/score", response_class=HTMLResponse)
async def score(
    request: Request,
    instrument: str = Form(...),
    respondent_id: Optional[str] = Form("participant_id"),
    data_file: UploadFile = File(...),
):
    context = _base_context(request)
    context["active_tab"] = "score"
    try:
        df = _read_csv(data_file)
        spec = load_instrument_spec(instrument)
        scored = score_responses(spec, df, respondent_id_col=respondent_id)
        context["score_table"] = scored.to_html(classes="table table-striped table-sm", index=False)
        context["score_csv"] = scored.to_csv(index=False)
        context["success_message"] = f"Scored {len(scored)} rows for {spec['instrument']['name']}."
    except (ValueError, ScoringError, UnicodeDecodeError) as exc:
        context["error_message"] = f"Scoring failed: {exc}"
    return templates.TemplateResponse("index.html", context)


@app.post("/summary", response_class=HTMLResponse)
async def summary(
    request: Request,
    instrument: str = Form(...),
    scored_file: UploadFile = File(...),
):
    context = _base_context(request)
    context["active_tab"] = "summary"
    try:
        df = _read_csv(scored_file)
        spec = load_instrument_spec(instrument)
        stats = summarize_scores(spec, df)
        context["summary_data"] = stats
        context["success_message"] = f"Loaded summary for {spec['instrument']['name']}."
    except (ValueError, ScoringError, UnicodeDecodeError) as exc:
        context["error_message"] = f"Summary failed: {exc}"
    return templates.TemplateResponse("index.html", context)


@app.post("/plot", response_class=HTMLResponse)
async def plot(
    request: Request,
    instrument_name: str = Form(...),
    panel_file: UploadFile = File(...),
):
    context = _base_context(request)
    context["active_tab"] = "plot"
    try:
        df = _read_csv(panel_file)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        output = plot_panel(df, instrument_name=instrument_name, save_path=tmp_path)
        encoded = base64.b64encode(output.read_bytes()).decode("ascii")
        output.unlink(missing_ok=True)
        context["plot_data_uri"] = f"data:image/png;base64,{encoded}"
        context["success_message"] = f"Generated plot for {instrument_name}."
    except (ValueError, UnicodeDecodeError) as exc:
        context["error_message"] = f"Plotting failed: {exc}"
    return templates.TemplateResponse("index.html", context)
