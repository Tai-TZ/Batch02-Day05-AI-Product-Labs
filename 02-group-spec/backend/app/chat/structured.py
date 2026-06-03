from __future__ import annotations

from typing import Any


def build_structured_from_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    structured: dict[str, Any] = {}
    for ev in events:
        result = (ev.get("result") or {})
        tool = ev.get("tool")
        if tool == "get_ticket_prices" and "tickets" in result:
            structured["priceQuote"] = {
                "supplierCode": result.get("supplierCode"),
                "usingDate": result.get("usingDate"),
                "siteName": result.get("siteName"),
                "tickets": result.get("tickets", []),
            }
        if tool == "get_weather_forecast" and result.get("summary"):
            structured["weather"] = {
                "location": result.get("location"),
                "date": result.get("date"),
                "summary": result.get("summary"),
            }
        if tool == "resolve_site" and result.get("site_code"):
            structured["destinationMap"] = {
                "destinationName": result.get("destination_name"),
                "siteCode": result.get("site_code"),
                "siteName": result.get("site_name"),
            }
    return structured


def build_dashboard_from_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    dashboard: dict[str, Any] = {"focus": "idle"}
    for ev in events:
        result = ev.get("result") or {}
        if ev.get("tool") == "resolve_site" and result.get("site_code"):
            dashboard = {
                "focus": "destination",
                "destination": {
                    "region": result.get("destination_name"),
                    "siteName": result.get("site_name"),
                    "supplierCode": result.get("site_code"),
                    "usingDate": "",
                },
            }
        if ev.get("tool") == "get_ticket_prices" and result.get("tickets"):
            dashboard["focus"] = "prices"
            dashboard["priceQuote"] = {
                "supplierCode": result.get("supplierCode"),
                "usingDate": result.get("usingDate"),
                "siteName": result.get("siteName"),
                "tickets": result.get("tickets", []),
            }
        if ev.get("tool") == "get_weather_forecast":
            dashboard["focus"] = "weather"
            dashboard["weather"] = {
                "location": result.get("location"),
                "summary": result.get("summary"),
            }
    return dashboard
