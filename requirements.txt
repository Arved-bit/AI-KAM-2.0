"""Indlæsning af struktureret demo-intelligence til briefingmotoren."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "demo_data"


def load_company_intelligence(company_name: str) -> dict[str, Any]:
    """Indlæser den strukturerede profil for den valgte demokunde."""
    slug = company_name.strip().casefold().replace(" ", "_")
    data_path = DATA_DIRECTORY / f"{slug}.json"
    if not data_path.is_file():
        available = ", ".join(path.stem.replace("_", " ") for path in DATA_DIRECTORY.glob("*.json"))
        raise ValueError(f"Der findes ingen intelligence-profil for '{company_name}'. Vælg: {available}.")
    with data_path.open(encoding="utf-8") as data_file:
        return json.load(data_file)
