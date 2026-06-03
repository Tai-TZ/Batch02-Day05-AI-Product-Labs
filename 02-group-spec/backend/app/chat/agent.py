from __future__ import annotations

import time
import uuid
from typing import Any, Generator

from app.chat.structured import build_dashboard_from_events, build_structured_from_events
from app.chat.tool_loop import run_model_tool_loop
from app.config import ARTIFACTS_DIR, settings
from app.providers import get_llm_provider, llm_configured
from app.providers.openrouter import OpenRouterProvider
from app.tools.declarations import load_tool_declarations, to_openai_tools
from app.tools.registry import execute_tool


def _new_step(
    *,
    phase: str,
    title: str,
    detail: str = "",
    tool: str | None = None,
    status: str = "running",
    source: str = "system",
) -> dict[str, Any]:
    return {
        "id": uuid.uuid4().hex[:12],
        "phase": phase,
        "title": title,
        "detail": detail,
        "tool": tool,
        "status": status,
        "source": source,
    }


class VinWondersAgent:
    """Skeleton agent: OpenRouter + tool loop (Day 04) + SSE events (Day 03 C2)."""

    def __init__(self, provider: OpenRouterProvider | None = None) -> None:
        self.provider = provider or get_llm_provider()
        self.tool_declarations = load_tool_declarations()
        self.openai_tools = to_openai_tools(self.tool_declarations)
        self.system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
        self._ui_steps: list[dict[str, Any]] = []
        self._tool_events: list[dict[str, Any]] = []

    def _build_messages(self, user_message: str, conversation_context: str | None) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = [
            {"role": "system", "content": self.system_prompt},
        ]
        if conversation_context:
            messages.append(
                {
                    "role": "user",
                    "content": f"Lịch sử hội thoại:\n{conversation_context}",
                }
            )
        messages.append({"role": "user", "content": user_message})
        return messages

    def run(self, user_message: str, *, conversation_context: str | None = None) -> str:
        cfg = settings()
        if cfg["demo_mode"] or not llm_configured():
            return self._demo_reply(user_message)
        text, events, _ = run_model_tool_loop(
            self.provider,
            self._build_messages(user_message, conversation_context),
            self.openai_tools,
            max_rounds=cfg["max_tool_rounds"],
        )
        self._tool_events = events
        return text

    def _demo_reply(self, user_message: str) -> str:
        site = execute_tool("resolve_site", {"query": user_message})
        return (
            "🤖 **Chế độ demo** (chưa có OPENROUTER_API_KEY).\n\n"
            f"Bạn hỏi: _{user_message}_\n\n"
            f"Gợi ý địa điểm: `{site}`\n\n"
            "Thêm key vào `backend/.env` hoặc tắt DEMO_MODE để bật agent thật."
        )

    def run_with_events(
        self,
        user_message: str,
        *,
        conversation_context: str | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        cfg = settings()
        self._ui_steps = []
        self._tool_events = []

        init = _new_step(phase="init", title="Khởi tạo agent VinWonders", status="done")
        self._ui_steps.append(init)
        yield {"type": "agent_step", "step": init}

        if cfg["demo_mode"] or not llm_configured():
            yield from self._stream_demo(user_message)
            return

        reasoning = _new_step(
            phase="reasoning",
            title="Phân tích yêu cầu khách",
            detail=user_message[:120],
            status="running",
            source="model",
        )
        self._ui_steps.append(reasoning)
        yield {"type": "agent_step", "step": reasoning}

        messages = self._build_messages(user_message, conversation_context)
        tool_events: list[dict[str, Any]] = []

        for round_idx in range(cfg["max_tool_rounds"]):
            response = self.provider.complete(messages, self.openai_tools)
            if not response.tool_calls:
                reasoning["status"] = "done"
                yield {"type": "agent_step", "step": reasoning}
                final = (response.text or "").strip() or "Xin lỗi, tôi chưa có câu trả lời."
                yield from self._emit_structured(tool_events)
                yield from self._stream_tokens(final)
                yield from self._emit_done()
                return

            for call in response.tool_calls:
                step = _new_step(
                    phase="tool",
                    title=f"Gọi tool: {call.name}",
                    detail=str(call.args)[:200],
                    tool=call.name,
                    status="running",
                    source="model",
                )
                self._ui_steps.append(step)
                yield {"type": "agent_step", "step": step}

                from app.tools.registry import execute_tool_call

                event = execute_tool_call(call.name, call.args)
                tool_events.append(event)
                step["status"] = "done"
                step["title"] = f"Observation — {call.name}"
                step["observationPreview"] = str(event.get("result"))[:240]
                yield {"type": "agent_step", "step": step}

            from app.tools.registry import tool_results_message
            from app.chat.tool_loop import assistant_tool_message

            messages.append(assistant_tool_message(response.text, response.tool_calls))
            messages.append(tool_results_message(tool_events))

        yield from self._emit_structured(tool_events)
        fallback = "Đã đạt giới hạn tool rounds — vui lòng hỏi cụ thể hơn (địa điểm, ngày đi)."
        yield from self._stream_tokens(fallback)
        yield from self._emit_done()

    def _emit_structured(self, tool_events: list[dict[str, Any]]):
        self._tool_events = tool_events
        structured = build_structured_from_events(tool_events)
        dashboard = build_dashboard_from_events(tool_events)
        if structured:
            yield {"type": "structured", "data": structured}
        if dashboard.get("focus") != "idle":
            yield {"type": "dashboard", "data": dashboard}

    def _stream_tokens(self, text: str):
        chunk_size = 24
        for i in range(0, len(text), chunk_size):
            yield {"type": "content", "delta": text[i : i + chunk_size]}
            time.sleep(0.02)

    def _emit_done(self):
        tool_count = len([s for s in self._ui_steps if s.get("phase") == "tool" and s.get("status") == "done"])
        yield {
            "type": "agent_done",
            "run": {
                "steps": self._ui_steps,
                "toolCount": tool_count,
                "reactSteps": tool_count,
            },
        }

    def _stream_demo(self, user_message: str) -> Generator[dict[str, Any], None, None]:
        resolve_ev = execute_tool("resolve_site", {"query": user_message})
        self._tool_events = [{"tool": "resolve_site", "args": {"query": user_message}, "result": resolve_ev}]
        site_code = resolve_ev.get("site_code") or "NTVW1"
        price_ev = execute_tool(
            "get_ticket_prices",
            {"site_code": site_code, "visit_date": "01-06-2026"},
        )
        self._tool_events.append(
            {
                "tool": "get_ticket_prices",
                "args": {"site_code": site_code, "visit_date": "01-06-2026"},
                "result": price_ev,
            }
        )

        for ev in self._tool_events:
            step = _new_step(
                phase="tool",
                title=f"Demo — {ev['tool']}",
                detail=str(ev.get("result"))[:120],
                tool=ev["tool"],
                status="done",
                source="system",
            )
            self._ui_steps.append(step)
            yield {"type": "agent_step", "step": step}
            time.sleep(0.15)

        yield from self._emit_structured(self._tool_events)
        reply = self._demo_reply(user_message)
        yield from self._stream_tokens(reply)
        yield from self._emit_done()
