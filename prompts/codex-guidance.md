# Codex Guidance

- Validate scoring changes with `pytest tests/test_scoring.py` plus the CLI smoke test in `scripts/run-tests.sh`.
- Keep the instrument YAML schemas backwards compatible; update `README.md` whenever fields move.
- Store any demo data inside `examples/` only; never mix with production survey exports.
- Summaries of UX or scoring tweaks belong in `CHANGELOG.md` and should reference the matching roadmap objective.
