from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.providers.base import BaseProvider


class DemoDataProvider(BaseProvider):
    def __init__(self, domain: str) -> None:
        super().__init__(provider="demo", domain=domain)
        self._base_path = Path(__file__).resolve().parent.parent / "data" / "demo"
        self.mark_demo()

    async def load(self, dataset: str) -> Any:
        path = self._base_path / f"{dataset}.json"
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.mark_demo(f"Serving demo dataset '{dataset}'.")
        return payload

