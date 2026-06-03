from __future__ import annotations

import json
from typing import Any, Callable

from app.vinwonders.destinations import list_destination_names, match_region
from app.vinwonders.prices import get_ticket_prices


def tool_list_destinations() -> dict[str, Any]:
    return {"destinations": list_destination_names()}


def tool_resolve_site(query: str) -> dict[str, Any]:
    region = match_region(query)
    if not region:
        return {"error": "not_found", "query": query}
    subs = region.get("sub_locations") or []
    primary = subs[0] if subs else {}
    return {
        "destination_name": region.get("destination_name"),
        "destination_code": region.get("destination_code"),
        "site_code": primary.get("code"),
        "site_name": primary.get("name"),
        "sub_locations": subs,
    }


def tool_get_ticket_prices(site_code: str, visit_date: str) -> dict[str, Any]:
    return get_ticket_prices(site_code, visit_date)


def tool_get_weather_forecast(location: str, date: str = "") -> dict[str, Any]:
    return {
        "location": location,
        "date": date or "hôm nay",
        "summary": "Nắng nhẹ, 28–32°C (mock — thêm OPENWEATHER_API_KEY để live)",
        "source": "mock",
    }


TOOL_FUNCTIONS: dict[str, Callable[..., dict[str, Any]]] = {
    "list_destinations": tool_list_destinations,
    "resolve_site": tool_resolve_site,
    "get_ticket_prices": tool_get_ticket_prices,
    "get_weather_forecast": tool_get_weather_forecast,
}


def execute_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return {"error": "unknown_tool", "tool": name}
    try:
        return func(**args)
    except TypeError as exc:
        return {"error": "bad_args", "tool": name, "message": str(exc), "args": args}
    except Exception as exc:
        return {"error": type(exc).__name__, "tool": name, "message": str(exc)}


def execute_tool_call(call_name: str, call_args: dict[str, Any]) -> dict[str, Any]:
    return {"tool": call_name, "args": call_args, "result": execute_tool(call_name, call_args)}


def tool_results_message(events: list[dict[str, Any]]) -> dict[str, str]:
    payload = json.dumps(events, ensure_ascii=False, indent=2)
    return {
        "role": "user",
        "content": (
            "TOOL_RESULTS_JSON:\n"
            f"{payload}\n\n"
            "Dùng kết quả tool ở trên. Trả lời khách bằng tiếng Việt, ngắn gọn, thân thiện."
        ),
    }
