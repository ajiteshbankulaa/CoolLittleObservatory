from __future__ import annotations

from datetime import date
from typing import Any

import httpx

from app.core.config import Settings
from app.providers.base import BaseProvider


class NasaProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(provider="nasa", domain="nasa")
        self._settings = settings

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        params = {**(params or {}), "api_key": self._settings.nasa_api_key}
        timeout = httpx.Timeout(self._settings.request_timeout_seconds)
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.get(f"{self._settings.nasa_api_base}{path}", params=params)
                    response.raise_for_status()
                    self.record_success(f"Fetched {path}.")
                    return response.json()
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt == 2:
                    break
        if last_error is not None:
            raise last_error
        raise RuntimeError(f"Request failed for {path}")

    async def fetch_apod(self) -> Any:
        try:
            return await self._get("/planetary/apod")
        except Exception as exc:
            self.record_failure(f"APOD fetch failed: {exc}")
            raise

    async def fetch_neo_feed(self, start: date, end: date) -> Any:
        try:
            return await self._get(
                "/neo/rest/v1/feed",
                params={
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                },
            )
        except Exception as exc:
            self.record_failure(f"NEO feed fetch failed: {exc}")
            raise
