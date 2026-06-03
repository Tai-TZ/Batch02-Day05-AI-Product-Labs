from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)
    stream: bool = False


class LegacyChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    mode: str = Field(default="agent", pattern="^(agent|chatbot)$")
    provider: str | None = None


class LegacyChatResponse(BaseModel):
    reply: str
    reasoning_steps: list[str] = Field(default_factory=list)
    mode: str
    provider: str = ""
