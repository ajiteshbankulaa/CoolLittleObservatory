from __future__ import annotations

from app.models.common import ApiResponse, SourceInfo
from app.models.search import SearchResult
from app.services.deep_space import DeepSpaceService
from app.services.featured import FeaturedService
from app.services.helpers import build_freshness, utc_now
from app.services.neo import NeoService
from app.services.orbit import OrbitService
from app.services.solar_system import SolarSystemService


class SearchService:
    def __init__(
        self,
        orbit_service: OrbitService,
        solar_system_service: SolarSystemService,
        neo_service: NeoService,
        deep_space_service: DeepSpaceService,
        featured_service: FeaturedService,
    ) -> None:
        self._orbit_service = orbit_service
        self._solar_system_service = solar_system_service
        self._neo_service = neo_service
        self._deep_space_service = deep_space_service
        self._featured_service = featured_service

    async def search(self, query: str, limit: int = 10) -> ApiResponse[list[SearchResult]]:
        needle = query.strip().lower()
        orbit = await self._orbit_service.get_overview()
        solar = await self._solar_system_service.list_bodies()
        neo = await self._neo_service.get_feed()
        deep = await self._deep_space_service.list_objects()
        tours = await self._featured_service.list_tours()

        results: list[SearchResult] = []
        for item in orbit.data.featured + orbit.data.stations + orbit.data.satellites:
            haystack = " ".join([item.name, item.description, *item.tags]).lower()
            if needle in haystack:
                results.append(
                    SearchResult(
                        id=item.id,
                        name=item.name,
                        mode="earth-orbit",
                        category=item.category,
                        summary=item.description,
                        tags=item.tags,
                        freshness_label=orbit.freshness.label,
                    )
                )
        for item in solar.data:
            haystack = " ".join([item.name, item.description, *item.tags]).lower()
            if needle in haystack:
                results.append(
                    SearchResult(
                        id=item.id,
                        name=item.name,
                        mode="solar-system",
                        category=item.kind,
                        summary=item.description,
                        tags=item.tags,
                        freshness_label=solar.freshness.label,
                    )
                )
        for item in neo.data:
            haystack = " ".join([item.name, item.description, *item.tags]).lower()
            if needle in haystack:
                results.append(
                    SearchResult(
                        id=item.id,
                        name=item.name,
                        mode="neo",
                        category=item.orbit_class or "neo",
                        summary=item.description,
                        tags=item.tags,
                        freshness_label=neo.freshness.label,
                    )
                )
        for item in deep.data:
            haystack = " ".join([item.name, item.description, *item.tags]).lower()
            if needle in haystack:
                results.append(
                    SearchResult(
                        id=item.id,
                        name=item.name,
                        mode="deep-space",
                        category=item.category,
                        summary=item.description,
                        tags=item.tags,
                        freshness_label=deep.freshness.label,
                    )
                )
        for item in tours.data:
            haystack = " ".join([item.title, item.summary, *item.tags]).lower()
            if needle in haystack:
                results.append(
                    SearchResult(
                        id=item.id,
                        name=item.title,
                        mode="featured-tour",
                        category="tour",
                        summary=item.summary,
                        tags=item.tags,
                        freshness_label=tours.freshness.label,
                    )
                )

        updated_at = utc_now()
        return ApiResponse(
            status="ok",
            freshness=build_freshness(classification="curated", updated_at=updated_at),
            warnings=[],
            sources=[
                SourceInfo(
                    provider="aggregated-search",
                    dataset="cross-mode search index",
                    classification="curated",
                    status="ok",
                    fetched_at=updated_at,
                )
            ],
            data=results[:limit],
        )
