from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.config import DATA_DIR

DESTINATIONS_PATH = DATA_DIR / "destinations.json"


def normalize_text(value: str) -> str:
    text = value.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


@lru_cache(maxsize=1)
def load_destinations() -> dict[str, Any]:
    return json.loads(DESTINATIONS_PATH.read_text(encoding="utf-8"))


def list_destination_names() -> list[str]:
    return [
        r.get("destination_name", "")
        for r in load_destinations().get("destinations", [])
        if r.get("destination_name")
    ]


def _region_score(query: str, region_name: str) -> int:
    q = normalize_text(query)
    rn = normalize_text(region_name)
    if not q or not rn:
        return 0
    if q == rn:
        return 100
    if q in rn or rn in q:
        return 80
    if any(tok in rn for tok in q.split() if len(tok) > 2):
        return 50
    return 0


def match_region(query: str) -> dict[str, Any] | None:
    if not query.strip():
        return None
    best: tuple[int, dict[str, Any]] | None = None
    for region in load_destinations().get("destinations", []):
        name = region.get("destination_name", "")
        score = _region_score(query, name)
        if score > 0 and (best is None or score > best[0]):
            best = (score, region)
    return best[1] if best else None


def find_site_by_code(code: str) -> dict[str, Any] | None:
    code_u = code.strip().upper()
    for region in load_destinations().get("destinations", []):
        for sub in region.get("sub_locations") or []:
            if (sub.get("code") or "").upper() == code_u:
                return {
                    "destination_name": region.get("destination_name"),
                    "destination_code": region.get("destination_code"),
                    **sub,
                }
    return None
