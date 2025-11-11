from pathlib import Path

from typer.testing import CliRunner

from psylab.cli import app


runner = CliRunner()


def test_score_csv_command(tmp_path: Path):
    output_path = tmp_path / "scores.csv"
    result = runner.invoke(
        app,
        [
            "score-csv",
            "phq9",
            "examples/sample_phq9.csv",
            "--out",
            str(output_path),
        ],
    )
    assert result.exit_code == 0
    assert output_path.exists()
    text = output_path.read_text().strip().splitlines()[1]
    assert text.startswith("phq9")


def test_instruments_listing():
    result = runner.invoke(app, ["instruments"])
    assert result.exit_code == 0
    assert "PHQ-9" in result.stdout
    assert "PCL-5" in result.stdout
    assert "BDI-II" in result.stdout


def test_instruments_json():
    result = runner.invoke(app, ["instruments", "--json"])
    assert result.exit_code == 0
    payload = result.stdout.strip()
    assert payload.startswith("[")
    assert '"id": "phq9"' in payload
    assert '"name": "PHQ-9"' in payload
