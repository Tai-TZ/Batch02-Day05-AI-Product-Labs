from __future__ import annotations

import json
from typing import Any


def sse_payload(obj: dict[str, Any]) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def sse_done() -> str:
    return "data: [DONE]\n\n"
