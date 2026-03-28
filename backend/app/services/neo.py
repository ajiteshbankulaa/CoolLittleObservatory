from __future__ import annotations

import math
from datetime import date, datetime, timedelta, timezone

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.models.common import ApiResponse, SourceInfo, WarningInfo
from app.models.neo import NeoObject
from app.models.solar_system import Vector3
from app.providers.demo import DemoDataProvider
from app.providers.nasa import NasaProvider
from app.services.helpers import build_freshness, utc_now


AU_IN_KM = 149_597_870.7


class NeoService:
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
        await self.get_feed()

    async def get_feed(self, start: date | None = None, end: date | None = None) -> ApiResponse[list[NeoObject]]:
        start = start or date.today()
        end = end or (start + timedelta(days=6))
        cache_key = f"neo:{start.isoformat()}:{end.isoformat()}"
        cached = await self._cache.get(cache_key)
        if cached and not cached.expired:
            return cached.value  # type: ignore[return-value]

        response = await self._build_response(start=start, end=end)
        await self._cache.set(cache_key, response, self._settings.neo_cache_ttl_seconds)
        return response

    async def _build_response(self, start: date, end: date) -> ApiResponse[list[NeoObject]]:
        warnings: list[WarningInfo] = []
        if not self._settings.universe_demo_mode and self._settings.enable_live_providers:
            try:
                raw = await self._nasa_provider.fetch_neo_feed(start, end)
                normalized = self._normalize_live_feed(raw)
                updated_at = utc_now()
                return ApiResponse(
                    status="ok",
                    freshness=build_freshness(
                        classification="refreshed",
                        updated_at=updated_at,
                        ttl_seconds=self._settings.neo_cache_ttl_seconds,
                    ),
                    warnings=[],
                    sources=[
                        SourceInfo(
                            provider="nasa",
                            dataset="NeoWs feed",
                            classification="refreshed",
                            status="ok",
                            fetched_at=updated_at,
                            url="https://api.nasa.gov/",
                        )
                    ],
                    data=normalized,
                )
            except Exception:
                warnings.append(
                    WarningInfo(
                        code="neo_fallback_demo",
                        message="Live NEO feed unavailable, serving curated close-approach examples.",
                    )
                )

        raw = await self._demo_provider.load("neo")
        updated_at = utc_now()
        return ApiResponse(
            status="demo" if self._settings.universe_demo_mode else "degraded",
            freshness=build_freshness(
                classification="demo",
                updated_at=updated_at,
                ttl_seconds=self._settings.neo_cache_ttl_seconds,
            ),
            warnings=warnings,
            sources=[
                SourceInfo(
                    provider="demo",
                    dataset="built-in NEO feed",
                    classification="demo",
                    status="demo",
                    fetched_at=updated_at,
                )
            ],
            data=[NeoObject(**item) for item in raw["objects"]],
        )

    def _normalize_live_feed(self, payload: dict[str, object]) -> list[NeoObject]:
        objects: list[NeoObject] = []
        feed = payload.get("near_earth_objects", {})
        index = 0
        for entries in feed.values():
            for item in entries:
                approaches = item.get("close_approach_data", [])
                if not approaches:
                    continue
                approach = approaches[0]
                miss_distance_km = float(approach["miss_distance"]["kilometers"])
                distance_au = miss_distance_km / AU_IN_KM
                phase = 0.65 * index
                position = Vector3(
                    x=1.0 + math.cos(phase) * distance_au,
                    y=0.0,
                    z=math.sin(phase) * distance_au,
                )
                close_approach = approach.get("close_approach_date_full") or f"{approach['close_approach_date']} 00:00"
                objects.append(
                    NeoObject(
                        id=str(item["id"]),
                        name=str(item["name"]),
                        designation=str(item["name"]),
                        is_hazardous=bool(item["is_potentially_hazardous_asteroid"]),
                        close_approach=datetime.fromisoformat(close_approach.replace(" ", "T")).replace(tzinfo=timezone.utc),
                        miss_distance_km=miss_distance_km,
                        relative_velocity_kps=float(approach["relative_velocity"]["kilometers_per_second"]),
                        estimated_diameter_min_m=float(item["estimated_diameter"]["meters"]["estimated_diameter_min"]),
                        estimated_diameter_max_m=float(item["estimated_diameter"]["meters"]["estimated_diameter_max"]),
                        orbit_class=item.get("orbital_data", {}).get("orbit_class", {}).get("orbit_class_type"),
                        position_au=position,
                        description="Refreshed from NASA NeoWs close-approach feed.",
                        tags=["neo", "close-approach", "nasa"],
                    )
                )
                index += 1
        return sorted(objects, key=lambda item: item.close_approach)
