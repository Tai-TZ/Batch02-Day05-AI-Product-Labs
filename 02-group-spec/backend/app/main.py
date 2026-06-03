"""FastAPI — VinWonders chat agent + data API for group demo."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.chat.agent import VinWondersAgent
from app.config import settings
from app.models import ChatMessage, ChatRequest, LegacyChatRequest, LegacyChatResponse
from app.providers import llm_configured
from app.providers.openrouter import OpenRouterProvider
from app.sse import sse_done, sse_payload
from app.vinwonders.destinations import load_destinations
from app.vinwonders.prices import get_ticket_prices

app = FastAPI(title="VinWonders Group API", version="0.1.0")

_cfg = settings()
_cors = _cfg["cors_origins"]
_use_wildcard = "*" in _cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _use_wildcard else _cors,
    allow_origin_regex=r"https://.*\.trycloudflare\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _normalize_date(date: str) -> str:
    if re.match(r"^\d{2}-\d{2}-\d{4}$", date):
        return date
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        y, m, d = date.split("-")
        return f"{d}-{m}-{y}"
    raise HTTPException(400, "date must be DD-MM-YYYY or YYYY-MM-DD")


def _conversation_context(messages: list[ChatMessage]) -> str | None:
    if len(messages) <= 1:
        return None
    lines: list[str] = []
    for m in messages[:-1]:
        role = "Khách" if m.role == "user" else "AI"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines[-10:])


def _latest_user_message(messages: list[ChatMessage]) -> str:
    for m in reversed(messages):
        if m.role == "user":
            return m.content
    raise HTTPException(400, "No user message in request")


@lru_cache(maxsize=1)
def _get_agent() -> VinWondersAgent:
    return VinWondersAgent()


def _event_to_sse(event: dict[str, Any]) -> dict[str, Any] | None:
    if event.get("type") == "content":
        return {
            "choices": [{"delta": {"content": event.get("delta", "")}}],
        }
    if event.get("type") in {
        "agent_step",
        "agent_done",
        "structured",
        "dashboard",
        "trace",
        "error",
    }:
        return event
    return None


@app.get("/api/health")
def health():
    provider = settings()["agent_provider"]
    model = OpenRouterProvider().default_model
    llm_ok = llm_configured()
    return {
        "status": "ok",
        "provider": provider,
        "model": model,
        "llm": {"ok": llm_ok, "error": None if llm_ok else "Missing OPENROUTER_API_KEY"},
    }


@app.get("/health")
def health_root():
    return health()


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    if body.get("stream"):
        raise HTTPException(400, "Use POST /api/chat/stream for streaming")

    if "message" in body and "messages" not in body:
        req = LegacyChatRequest.model_validate(body)
        agent = _get_agent()
        reply = agent.run(req.message.strip())
        return LegacyChatResponse(
            reply=reply,
            reasoning_steps=[s.get("title", "") for s in getattr(agent, "_ui_steps", [])],
            mode=req.mode,
            provider=settings()["agent_provider"],
        )

    req = ChatRequest.model_validate(body)
    try:
        agent = _get_agent()
        text = agent.run(
            _latest_user_message(req.messages),
            conversation_context=_conversation_context(req.messages),
        )
        return {
            "content": text,
            "model": agent.provider.model_name,
            "agent": True,
            "structured": {},
        }
    except Exception as exc:
        raise HTTPException(502, f"Agent error: {exc}") from exc


@app.post("/api/chat/stream")
def chat_stream(req: ChatRequest):
    agent = _get_agent()
    user_msg = _latest_user_message(req.messages)
    context = _conversation_context(req.messages)

    def generate():
        try:
            for event in agent.run_with_events(user_msg, conversation_context=context):
                payload = _event_to_sse(event)
                if payload:
                    yield sse_payload(payload)
            yield sse_done()
        except Exception as exc:
            yield sse_payload({"type": "error", "message": str(exc)})
            yield sse_done()

    return StreamingResponse(
        generate(),
        media_type="text/event-stream; charset=utf-8",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/destinations")
def destinations():
    return load_destinations()


@app.get("/api/prices")
def prices(
    code: str = Query(..., min_length=2),
    date: str = Query(..., description="DD-MM-YYYY or YYYY-MM-DD"),
    detailed: bool = Query(False),
):
    using_date = _normalize_date(date)
    try:
        return get_ticket_prices(code, using_date)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(502, f"Failed to fetch prices: {exc}") from exc
