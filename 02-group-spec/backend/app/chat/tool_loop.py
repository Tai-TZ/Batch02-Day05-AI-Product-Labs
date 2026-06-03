from __future__ import annotations

import json
from typing import Any

from app.providers.base import ToolCall
from app.providers.openrouter import OpenRouterProvider
from app.tools.registry import execute_tool_call, tool_results_message


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def assistant_tool_message(text: str | None, calls: list[ToolCall]) -> dict[str, str]:
    summary = [{"name": c.name, "args": c.args} for c in calls]
    content = text or "Đang gọi tool..."
    return {
        "role": "assistant",
        "content": f"{content}\n\nTOOL_CALLS_JSON:\n{_json_text(summary)}",
    }


def run_model_tool_loop(
    provider: OpenRouterProvider,
    messages: list[dict[str, str]],
    openai_tools: list[dict[str, Any]],
    *,
    max_rounds: int = 4,
) -> tuple[str, list[dict[str, Any]], str]:
    """
    Day 04-style multi-round tool loop.
    Returns (final_text, tool_events, status).
    """
    tool_events: list[dict[str, Any]] = []
    working = list(messages)

    for _ in range(max_rounds):
        response = provider.complete(working, openai_tools)
        if not response.tool_calls:
            text = (response.text or "").strip()
            return text or "Xin lỗi, tôi chưa có câu trả lời.", tool_events, "done"

        working.append(assistant_tool_message(response.text, response.tool_calls))
        round_events: list[dict[str, Any]] = []
        for call in response.tool_calls:
            round_events.append(execute_tool_call(call.name, call.args))
        tool_events.extend(round_events)
        working.append(tool_results_message(round_events))

    return (
        "Đã đạt giới hạn số vòng gọi tool. Vui lòng thu hẹp yêu cầu.",
        tool_events,
        "max_tool_rounds",
    )
