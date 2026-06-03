from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / "artifacts"
DATA_DIR = ROOT / "data"

load_dotenv(ROOT / ".env", override=True)


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@lru_cache(maxsize=1)
def settings() -> dict:
    return {
        "root": ROOT,
        "artifacts_dir": ARTIFACTS_DIR,
        "data_dir": DATA_DIR,
        "api_host": os.getenv("API_HOST", "0.0.0.0"),
        "api_port": int(os.getenv("API_PORT", "8000")),
        "agent_provider": os.getenv("AGENT_PROVIDER", "openrouter").lower(),
        "openrouter_model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        "demo_mode": env_bool("DEMO_MODE", False),
        "max_tool_rounds": int(os.getenv("CHAT_MAX_TOOL_ROUNDS", "4")),
        "history_window": int(os.getenv("CHAT_HISTORY_WINDOW", "5")),
        "prices_mode": os.getenv("PRICES_MODE", "mock").lower(),
        "cors_origins": [
            o.strip()
            for o in os.getenv(
                "CORS_ORIGINS",
                "http://localhost:8080,http://127.0.0.1:8080",
            ).split(",")
            if o.strip()
        ],
    }
