"""Run API: python run.py"""

from __future__ import annotations

import uvicorn

from app.config import settings


def main() -> None:
    cfg = settings()
    uvicorn.run(
        "app.main:app",
        host=cfg["api_host"],
        port=cfg["api_port"],
        reload=True,
    )


if __name__ == "__main__":
    main()
