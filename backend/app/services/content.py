from __future__ import annotations

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.models.common import ApiResponse, SourceInfo, WarningInfo
from app.models.content import ApodEntry
from app.providers.demo import DemoDataProvider
from app.providers.nasa import NasaProvider
from app.services.helpers import build_freshness, utc_now


class ContentService:
    def __init__(
        self,
        settings: Settings,
        cache: AsyncTTLCache,
        nasa_provider: NasaProvider,
        demo_provider: DemoDataProvider,
    ) -> None:
        self._settings = settings
        self._cache = cache
        self._nasa_provider = nasa_provider
        self._demo_provider = demo_provider

    async def prefetch(self) -> None:
        await self.get_apod()

    async def get_apod(self) -> ApiResponse[ApodEntry]:
        cache_key = "content:apod"
        cached = await self._cache.get(cache_key)
        if cached and not cached.expired:
            return cached.value  # type: ignore[return-value]

        warnings: list[WarningInfo] = []
        if not self._settings.universe_demo_mode and self._settings.enable_live_providers:
            try:
                payload = await self._nasa_provider.fetch_apod()
                updated_at = utc_now()
                response = ApiResponse(
                    status="ok",
                    freshness=build_freshness(
                        classification="refreshed",
                        updated_at=updated_at,
                        ttl_seconds=self._settings.content_cache_ttl_seconds,
                    ),
                    warnings=[],
                    sources=[
                        SourceInfo(
                            provider="nasa",
                            dataset="astronomy picture of the day",
                            classification="refreshed",
                            status="ok",
                            fetched_at=updated_at,
                            url="https://api.nasa.gov/",
                        )
                    ],
                    data=ApodEntry(**payload),
                )
                await self._cache.set(cache_key, response, self._settings.content_cache_ttl_seconds)
                return response
            except Exception:
                warnings.append(
                    WarningInfo(
                        code="apod_fallback_demo",
                        message="NASA APOD unavailable, serving demo editorial content.",
                    )
                )

        payload = await self._demo_provider.load("content")
        updated_at = utc_now()
        response = ApiResponse(
            status="demo" if self._settings.universe_demo_mode else "degraded",
            freshness=build_freshness(
                classification="demo",
                updated_at=updated_at,
                ttl_seconds=self._settings.content_cache_ttl_seconds,
            ),
            warnings=warnings,
            sources=[
                SourceInfo(
                    provider="demo",
                    dataset="editorial APOD fallback",
                    classification="demo",
                    status="demo",
                    fetched_at=updated_at,
                )
            ],
            data=ApodEntry(**payload["apod"]),
        )
        await self._cache.set(cache_key, response, self._settings.content_cache_ttl_seconds)
        return response
