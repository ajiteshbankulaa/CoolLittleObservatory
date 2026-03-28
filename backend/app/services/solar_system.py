from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.models.common import ApiResponse, SourceInfo
from app.models.solar_system import SolarBody, Vector3
from app.providers.demo import DemoDataProvider
from app.services.helpers import build_freshness, utc_now


REFERENCE_EPOCH = datetime(2026, 1, 1, tzinfo=timezone.utc)


@dataclass(slots=True)
class RawBody:
    id: str
    name: str
    kind: str
    description: str
    color: str
    radius_km: float
    semi_major_axis_au: float
    orbital_period_days: float | None
    phase_deg: float
    inclination_deg: float
    parent_id: str | None
    gravity_mps2: float | None
    tags: list[str]


class SolarSystemService:
    def __init__(self, settings: Settings, cache: AsyncTTLCache, demo_provider: DemoDataProvider) -> None:
        self._settings = settings
        self._cache = cache
        self._demo_provider = demo_provider

    async def prefetch(self) -> None:
        await self.list_bodies()

    async def list_bodies(self) -> ApiResponse[list[SolarBody]]:
        bundle = await self._load_bundle()
        return ApiResponse(
            status="ok",
            freshness=bundle["freshness"],
            warnings=[],
            sources=bundle["sources"],
            data=bundle["bodies"],
        )

    async def get_body(self, body_id: str) -> ApiResponse[SolarBody]:
        bundle = await self._load_bundle()
        item = bundle["index"].get(body_id)
        if item is None:
            raise KeyError(body_id)
        return ApiResponse(
            status="ok",
            freshness=bundle["freshness"],
            warnings=[],
            sources=bundle["sources"],
            data=item,
        )

    async def _load_bundle(self) -> dict[str, object]:
        cache_key = "solar:bundle"
        cached = await self._cache.get(cache_key)
        if cached and not cached.expired:
            return cached.value  # type: ignore[return-value]

        raw = await self._demo_provider.load("solar_system")
        raw_bodies = [RawBody(**item) for item in raw["bodies"]]
        raw_map = {body.id: body for body in raw_bodies}
        position_cache: dict[str, Vector3] = {}

        def position_for(body: RawBody) -> Vector3:
            if body.id in position_cache:
                return position_cache[body.id]
            if body.kind == "star":
                position = Vector3(x=0.0, y=0.0, z=0.0)
            else:
                days = (utc_now() - REFERENCE_EPOCH).total_seconds() / 86400
                angle = math.radians(body.phase_deg)
                if body.orbital_period_days:
                    angle += (days / body.orbital_period_days) * (2.0 * math.pi)
                inclination = math.radians(body.inclination_deg)
                local = Vector3(
                    x=body.semi_major_axis_au * math.cos(angle),
                    y=body.semi_major_axis_au * math.sin(inclination) * math.sin(angle),
                    z=body.semi_major_axis_au * math.cos(inclination) * math.sin(angle),
                )
                if body.parent_id:
                    parent = position_for(raw_map[body.parent_id])
                    position = Vector3(
                        x=parent.x + local.x,
                        y=parent.y + local.y,
                        z=parent.z + local.z,
                    )
                else:
                    position = local
            position_cache[body.id] = position
            return position

        def orbit_path_for(body: RawBody) -> list[Vector3]:
            if body.kind == "star" or body.semi_major_axis_au == 0:
                return []
            points: list[Vector3] = []
            parent_position = position_for(raw_map[body.parent_id]) if body.parent_id else Vector3(x=0, y=0, z=0)
            inclination = math.radians(body.inclination_deg)
            for step in range(64):
                angle = (step / 64) * (2.0 * math.pi)
                points.append(
                    Vector3(
                        x=parent_position.x + body.semi_major_axis_au * math.cos(angle),
                        y=parent_position.y + body.semi_major_axis_au * math.sin(inclination) * math.sin(angle),
                        z=parent_position.z + body.semi_major_axis_au * math.cos(inclination) * math.sin(angle),
                    )
                )
            return points

        bodies = [
            SolarBody(
                id=body.id,
                name=body.name,
                kind=body.kind,
                description=body.description,
                color=body.color,
                radius_km=body.radius_km,
                semi_major_axis_au=body.semi_major_axis_au,
                orbital_period_days=body.orbital_period_days,
                position_au=position_for(body),
                orbit_path_au=orbit_path_for(body),
                parent_id=body.parent_id,
                gravity_mps2=body.gravity_mps2,
                tags=body.tags,
            )
            for body in raw_bodies
        ]
        updated_at = utc_now()
        bundle = {
            "bodies": bodies,
            "index": {body.id: body for body in bodies},
            "sources": [
                SourceInfo(
                    provider="built-in-orbital-model",
                    dataset="curated solar system orbital model",
                    classification="refreshed",
                    status="ok",
                    fetched_at=updated_at,
                )
            ],
            "freshness": build_freshness(
                classification="refreshed",
                updated_at=updated_at,
                ttl_seconds=self._settings.solar_cache_ttl_seconds,
            ),
        }
        await self._cache.set(cache_key, bundle, self._settings.solar_cache_ttl_seconds)
        return bundle
