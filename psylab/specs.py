from __future__ import annotations

from functools import lru_cache
from importlib import resources
from typing import Any, Dict, List

import yaml


def _iter_instrument_files():
    package_root = resources.files(__package__) / "instruments"
    return [
        path
        for path in package_root.iterdir()
        if path.name.lower().endswith((".yaml", ".yml"))
    ]


@lru_cache(maxsize=None)
def _load_specs() -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    for path in _iter_instrument_files():
        with resources.as_file(path) as resolved:
            data = yaml.safe_load(resolved.read_text())
            data["_source_path"] = str(resolved)
            specs.append(data)
    return specs


def list_instruments() -> List[Dict[str, Any]]:
    """Return metadata for every bundled instrument."""
    specs = []
    for spec in _load_specs():
        info = spec.get("instrument", {})
        specs.append(
            {
                "id": info.get("id"),
                "name": info.get("name"),
                "version": info.get("version"),
                "description": info.get("description"),
            }
        )
    return sorted(specs, key=lambda row: row.get("name") or "")


def load_instrument_spec(identifier: str) -> Dict[str, Any]:
    """Load a YAML spec by id or instrument name."""
    if not identifier:
        raise ValueError("Instrument identifier is required")

    needle = identifier.strip().lower()
    for spec in _load_specs():
        info = spec.get("instrument", {})
        aliases = filter(None, [info.get("id"), info.get("name")])
        if any(needle == alias.lower() for alias in aliases):
            return spec

    raise KeyError(f"Instrument '{identifier}' is not registered")
