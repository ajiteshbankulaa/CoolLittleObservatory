from __future__ import annotations

from app.models.common import ApiResponse, SourceInfo
from app.models.content import FeaturedTour
from app.providers.demo import DemoDataProvider
from app.services.helpers import build_freshness, utc_now


class FeaturedService:
    def __init__(self, demo_provider: DemoDataProvider) -> None:
        self._demo_provider = demo_provider

    async def list_tours(self) -> ApiResponse[list[FeaturedTour]]:
        payload = await self._demo_provider.load("featured_tours")
        updated_at = utc_now()
        return ApiResponse(
            status="ok",
            freshness=build_freshness(classification="curated", updated_at=updated_at),
            warnings=[],
            sources=[
                SourceInfo(
                    provider="editorial-curation",
                    dataset="featured observatory tours",
                    classification="curated",
                    status="ok",
                    fetched_at=updated_at,
                )
            ],
            data=[FeaturedTour(**item) for item in payload["tours"]],
        )
