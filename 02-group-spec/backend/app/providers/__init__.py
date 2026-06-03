from __future__ import annotations

import os

from app.config import settings
from app.providers.openrouter import OpenRouterProvider


def get_llm_provider() -> OpenRouterProvider:
    name = settings()["agent_provider"]
    if name not in ("openrouter", "openai"):
        raise ValueError(f"Unsupported AGENT_PROVIDER: {name}")
    return OpenRouterProvider()


def llm_configured() -> bool:
    return bool(os.getenv("OPENROUTER_API_KEY", "").strip())
