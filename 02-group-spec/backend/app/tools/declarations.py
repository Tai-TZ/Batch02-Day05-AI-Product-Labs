from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from app.config import ARTIFACTS_DIR


def load_tool_declarations(path: Path | None = None) -> list[dict[str, Any]]:
    tools_path = path or (ARTIFACTS_DIR / "tools.yaml")
    data = yaml.safe_load(tools_path.read_text(encoding="utf-8")) or {}
    return list(data.get("tools") or [])


def to_openai_tools(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": item["name"],
                "description": item.get("description", ""),
                "parameters": item.get("parameters") or {"type": "object", "properties": {}},
            },
        }
        for item in declarations
    ]
