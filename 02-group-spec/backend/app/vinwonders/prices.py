from __future__ import annotations

import re
from typing import Any

from app.config import settings
from app.vinwonders.destinations import find_site_by_code


def _normalize_date(date: str) -> str:
    if re.match(r"^\d{2}-\d{2}-\d{4}$", date):
        return date
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        y, m, d = date.split("-")
        return f"{d}-{m}-{y}"
    raise ValueError("date must be DD-MM-YYYY or YYYY-MM-DD")


def _mock_prices(supplier_code: str, using_date: str) -> dict[str, Any]:
    site = find_site_by_code(supplier_code)
    site_name = (site or {}).get("name") or supplier_code
    return {
        "supplierCode": supplier_code,
        "usingDate": using_date,
        "siteName": site_name,
        "ticketCount": 2,
        "tickets": [
            {
                "name": f"Vé người lớn — {site_name}",
                "salePrice": 850_000,
                "originalPrice": 950_000,
                "guestType": "Người lớn",
                "isDefault": True,
            },
            {
                "name": f"Vé trẻ em — {site_name}",
                "salePrice": 650_000,
                "originalPrice": 720_000,
                "guestType": "Trẻ em",
                "isDefault": False,
            },
        ],
        "source": "mock",
    }


def _live_prices(supplier_code: str, using_date: str) -> dict[str, Any]:
    """Optional live crawl — same API as Day 3 C2 project."""
    import cloudscraper
    import requests

    api_tour = "https://booking-tour-api.vinpearl.com"
    api_info = f"{api_tour}/api/bwc/vinwonder/vinwonderinfo"
    api_detail = f"{api_tour}/api/bwc/vinwonder/vinwonderticketdetail"

    def referer() -> str:
        return (
            f"https://booking.vinwonders.com/vi-VND/search"
            f"?code={supplier_code}&usingDate={using_date}"
        )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Origin": "https://booking.vinwonders.com",
        "Referer": referer(),
        "x-supplier-code": supplier_code,
    }

    session = requests.Session()
    resp = session.get(
        api_info,
        params={"SupplierCode": supplier_code, "UsingDate": using_date},
        headers=headers,
        timeout=60,
    )
    resp.raise_for_status()
    batch = (resp.json().get("data") or {}).get("result") or []

    scraper = cloudscraper.create_scraper()
    tickets_out: list[dict[str, Any]] = []
    site_name = None

    for ticket in batch[:5]:
        site_name = site_name or ticket.get("vinWonderName")
        detail = scraper.get(
            api_detail,
            params={
                "SupplierCode": supplier_code,
                "UsingDate": using_date,
                "VinWonderTicketId": ticket.get("vinWonderTicketId"),
                "vinWonderId": ticket.get("vinWonderId"),
            },
            headers=headers,
            timeout=45,
        )
        detail.raise_for_status()
        tiers = (detail.json().get("data") or {}).get("result") or []
        for tier in tiers[:3]:
            tickets_out.append(
                {
                    "name": tier.get("ticketName") or ticket.get("vinWonderTicketName", "Vé"),
                    "salePrice": int(tier.get("salePrice") or 0),
                    "originalPrice": tier.get("originalPrice"),
                    "guestType": tier.get("guestTypeName") or "Standard",
                    "isDefault": bool(tier.get("isDefault")),
                }
            )

    return {
        "supplierCode": supplier_code,
        "usingDate": using_date,
        "siteName": site_name,
        "ticketCount": len(tickets_out),
        "tickets": tickets_out,
        "source": "live",
    }


def get_ticket_prices(supplier_code: str, visit_date: str) -> dict[str, Any]:
    using_date = _normalize_date(visit_date)
    mode = settings()["prices_mode"]
    if mode == "live":
        try:
            return _live_prices(supplier_code, using_date)
        except Exception:
            pass
    return _mock_prices(supplier_code, using_date)
