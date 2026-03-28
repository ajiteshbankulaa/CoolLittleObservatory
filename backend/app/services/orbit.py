from __future__ import annotations

import asyncio
import math
from datetime import datetime, timedelta

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.models.common import ApiResponse, SourceInfo, WarningInfo
from app.models.orbit import OrbitObject, OrbitOverview, OrbitPoint
from app.providers.demo import DemoDataProvider
from app.providers.orbit import CelesTrakOrbitProvider, TleRecord, propagate_record, record_epoch
from app.services.helpers import build_freshness, utc_now


def _category_for_group(group: str) -> tuple[str, str]:
    mapping = {
        "stations": ("station", "Crewed stations and orbital laboratories"),
        "science": ("science", "Research and Earth-observation spacecraft"),
        "weather": ("weather", "Weather and climate monitoring satellites"),
        "visual": ("communication", "Visually prominent satellites and spacecraft"),
    }
    return mapping.get(group, ("satellite", "Cataloged orbital asset"))


class OrbitService:
    def __init__(
        self,
        settings: Settings,
        cache: AsyncTTLCache,
        live_provider: CelesTrakOrbitProvider,
        demo_provider: DemoDataProvider,
    ) -> None:
        self._settings = settings
        self._cache = cache
        self._live_provider = live_provider
        self._demo_provider = demo_provider

    async def prefetch(self) -> None:
        await self.get_overview()

    async def get_overview(self) -> ApiResponse[OrbitOverview]:
        bundle = await self._load_bundle()
        overview = OrbitOverview(
            featured=bundle["featured"],
            stations=bundle["stations"],
            satellites=bundle["satellites"],
        )
        return ApiResponse(
            status=bundle["status"],
            freshness=bundle["freshness"],
            warnings=bundle["warnings"],
            sources=bundle["sources"],
            data=overview,
        )

    async def get_iss(self) -> ApiResponse[OrbitObject]:
        bundle = await self._load_bundle()
        for item in bundle["featured"] + bundle["stations"]:
            if item.norad_id == 25544 or "ISS" in item.name.upper():
                return ApiResponse(
                    status=bundle["status"],
                    freshness=bundle["freshness"],
                    warnings=bundle["warnings"],
                    sources=bundle["sources"],
                    data=item,
                )
        raise KeyError("ISS not available in orbit dataset")

    async def get_stations(self) -> ApiResponse[list[OrbitObject]]:
        bundle = await self._load_bundle()
        return ApiResponse(
            status=bundle["status"],
            freshness=bundle["freshness"],
            warnings=bundle["warnings"],
            sources=bundle["sources"],
            data=bundle["stations"],
        )

    async def get_satellites(self) -> ApiResponse[list[OrbitObject]]:
        bundle = await self._load_bundle()
        return ApiResponse(
            status=bundle["status"],
            freshness=bundle["freshness"],
            warnings=bundle["warnings"],
            sources=bundle["sources"],
            data=bundle["satellites"],
        )

    async def get_object(self, object_id: str) -> ApiResponse[OrbitObject]:
        bundle = await self._load_bundle()
        item = bundle["index"].get(object_id)
        if item is None:
            raise KeyError(object_id)
        return ApiResponse(
            status=bundle["status"],
            freshness=bundle["freshness"],
            warnings=bundle["warnings"],
            sources=bundle["sources"],
            data=item,
        )

    async def get_predictions(self, object_id: str) -> ApiResponse[list[OrbitPoint]]:
        bundle = await self._load_bundle()
        item = bundle["index"].get(object_id)
        if item is None:
            raise KeyError(object_id)
        return ApiResponse(
            status=bundle["status"],
            freshness=bundle["freshness"],
            warnings=bundle["warnings"],
            sources=bundle["sources"],
            data=item.ground_track,
        )

    async def _load_bundle(self) -> dict[str, object]:
        cache_key = "orbit:bundle"
        cached = await self._cache.get(cache_key)
        if cached and not cached.expired:
            return cached.value  # type: ignore[return-value]

        bundle = await self._build_bundle()
        await self._cache.set(cache_key, bundle, self._settings.orbit_cache_ttl_seconds)
        return bundle

    async def _build_bundle(self) -> dict[str, object]:
        if self._settings.universe_demo_mode or not self._settings.enable_live_providers:
            return await self._build_demo_bundle(status="demo", warnings=[])

        try:
            groups = ["stations", "science", "weather", "visual"]
            fetched = await asyncio.gather(*(self._live_provider.fetch_group(group) for group in groups))
            updated_at = utc_now()
            stations: list[OrbitObject] = []
            satellites: list[OrbitObject] = []
            featured: list[OrbitObject] = []
            index: dict[str, OrbitObject] = {}

            for records, group in zip(fetched, groups, strict=True):
                category, description = _category_for_group(group)
                limit = None if group == "stations" else self._settings.active_satellite_limit // 3 + 2
                for record in records[:limit]:
                    tracked = record.norad_id == 25544 or group == "stations"
                    item = self._normalize_live_record(
                        record,
                        category=category,
                        description=description,
                        tracked=tracked,
                    )
                    if group == "stations":
                        stations.append(item)
                    else:
                        satellites.append(item)
                    if tracked or len(featured) < 6:
                        featured.append(item)
                    index[item.id] = item

            source = SourceInfo(
                provider="celestrak",
                dataset="stations/science/weather/visual TLE groups",
                classification="near-live",
                status="ok",
                fetched_at=updated_at,
                url="https://celestrak.org/NORAD/elements/",
            )
            freshness = build_freshness(
                classification="near-live",
                updated_at=updated_at,
                ttl_seconds=self._settings.orbit_cache_ttl_seconds,
            )
            return {
                "status": "ok",
                "freshness": freshness,
                "warnings": [],
                "sources": [source],
                "featured": featured[:6],
                "stations": stations,
                "satellites": satellites[: self._settings.active_satellite_limit],
                "index": index,
            }
        except Exception as exc:
            self._live_provider.record_failure(f"Falling back to demo orbit data: {exc}")
            warning = WarningInfo(
                code="orbit_fallback_demo",
                message="Live orbit provider unavailable, serving curated demo tracks.",
            )
            return await self._build_demo_bundle(status="degraded", warnings=[warning])

    async def _build_demo_bundle(self, status: str, warnings: list[WarningInfo]) -> dict[str, object]:
        raw = await self._demo_provider.load("orbit")
        updated_at = utc_now()
        stations = [self._normalize_demo_object(item) for item in raw["stations"]]
        satellites = [self._normalize_demo_object(item) for item in raw["satellites"]]
        featured = [self._normalize_demo_object(item) for item in raw["featured"]]
        index = {item.id: item for item in featured + stations + satellites}
        source = SourceInfo(
            provider="demo",
            dataset="built-in orbit scene",
            classification="demo",
            status="demo",
            fetched_at=updated_at,
        )
        freshness = build_freshness(
            classification="demo",
            updated_at=updated_at,
            ttl_seconds=self._settings.orbit_cache_ttl_seconds,
        )
        return {
            "status": status,
            "freshness": freshness,
            "warnings": warnings,
            "sources": [source],
            "featured": featured,
            "stations": stations,
            "satellites": satellites,
            "index": index,
        }

    def _normalize_demo_object(self, raw: dict[str, object]) -> OrbitObject:
        trail = [OrbitPoint(**point) for point in raw.get("trail", [])]
        ground_track = [OrbitPoint(**point) for point in raw.get("ground_track", [])]
        return OrbitObject(
            id=str(raw["id"]),
            name=str(raw["name"]),
            norad_id=raw.get("norad_id"),
            category=raw["category"],
            subcategory=raw.get("subcategory"),
            description=str(raw["description"]),
            operator=raw.get("operator"),
            country=raw.get("country"),
            tags=list(raw.get("tags", [])),
            latitude=float(raw["latitude"]),
            longitude=float(raw["longitude"]),
            altitude_km=float(raw["altitude_km"]),
            speed_kps=float(raw["speed_kps"]),
            inclination_deg=raw.get("inclination_deg"),
            period_minutes=raw.get("period_minutes"),
            tle_epoch=datetime.fromisoformat(raw["tle_epoch"]) if raw.get("tle_epoch") else None,
            trail=trail,
            ground_track=ground_track,
            visibility=raw.get("visibility"),
            tracked=bool(raw.get("tracked", False)),
        )

    def _normalize_live_record(
        self,
        record: TleRecord,
        *,
        category: str,
        description: str,
        tracked: bool,
    ) -> OrbitObject:
        now = utc_now()
        track = []
        for offset in range(self._settings.orbit_prediction_steps):
            at = now + timedelta(minutes=offset * self._settings.orbit_prediction_step_minutes)
            track.append(propagate_record(record, at))
        current = track[0]
        period = None
        if record.satrec.no_kozai:
            period = (2.0 * math.pi) / record.satrec.no_kozai

        return OrbitObject(
            id=record.object_id,
            name=record.name,
            norad_id=record.norad_id,
            category=category,
            subcategory=record.group,
            description=f"{description}. Propagated from the latest public element set.",
            operator=None,
            country=None,
            tags=[record.group, "propagated", "celestrak"],
            latitude=current.latitude,
            longitude=current.longitude,
            altitude_km=current.altitude_km,
            speed_kps=current.speed_kps,
            inclination_deg=math.degrees(record.satrec.inclo),
            period_minutes=period,
            tle_epoch=record_epoch(record),
            trail=track[:6],
            ground_track=track,
            visibility="Predicted track",
            tracked=tracked,
        )
