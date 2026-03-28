from __future__ import annotations

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.models.common import ApiResponse, SourceInfo
from app.models.deep_space import DeepSpaceObject
from app.providers.demo import DemoDataProvider
from app.services.helpers import build_freshness, utc_now


class DeepSpaceService:
    def __init__(self, settings: Settings, cache: AsyncTTLCache, demo_provider: DemoDataProvider) -> None:
        self._settings = settings
        self._cache = cache
        self._demo_provider = demo_provider

    async def prefetch(self) -> None:
        await self.list_objects()

    async def list_objects(self, category: str | None = None) -> ApiResponse[list[DeepSpaceObject]]:
        cache_key = "deep-space:bundle"
        cached = await self._cache.get(cache_key)
        if cached and not cached.expired:
            response = cached.value  # type: ignore[assignment]
        else:
            raw = await self._demo_provider.load("deep_space")
            updated_at = utc_now()
            response = ApiResponse(
                status="ok",
                freshness=build_freshness(
                    classification="curated",
                    updated_at=updated_at,
                    ttl_seconds=self._settings.deep_space_cache_ttl_seconds,
                ),
                warnings=[],
                sources=[
                    SourceInfo(
                        provider="curated-catalog",
                        dataset="deep-space feature snapshot",
                        classification="curated",
                        status="ok",
                        fetched_at=updated_at,
                    )
                ],
                data=[DeepSpaceObject(**item) for item in raw["objects"]],
            )
            await self._cache.set(cache_key, response, self._settings.deep_space_cache_ttl_seconds)

        if category:
            filtered = [item for item in response.data if item.category == category]
            return response.model_copy(update={"data": filtered})
        return response
