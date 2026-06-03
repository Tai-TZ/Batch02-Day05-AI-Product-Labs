from __future__ import annotations

import json
import os
from typing import Any

from app.providers.base import ModelResponse, ToolCall


class OpenRouterProvider:
    """OpenAI-compatible Chat Completions (OpenRouter)."""

    def __init__(self) -> None:
        self.default_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        self.api_key_env = "OPENROUTER_API_KEY"
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    @property
    def model_name(self) -> str:
        return self.default_model

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.2,
    ) -> ModelResponse:
        from openai import OpenAI

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Missing {self.api_key_env}. Set DEMO_MODE=true or add key to .env"
            )

        client = OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost:8080"),
                "X-Title": os.getenv("OPENROUTER_APP_TITLE", "VinWonders Demo"),
            },
        )
        kwargs: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        resp = client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message
        calls: list[ToolCall] = []
        for call in msg.tool_calls or []:
            args = json.loads(call.function.arguments or "{}")
            calls.append(ToolCall(name=call.function.name, args=args))
        return ModelResponse(text=msg.content, tool_calls=calls, raw=resp)

    def stream_text(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
    ):
        from openai import OpenAI

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing {self.api_key_env}")

        client = OpenAI(api_key=api_key, base_url=self.base_url)
        stream = client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            temperature=0.3,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
