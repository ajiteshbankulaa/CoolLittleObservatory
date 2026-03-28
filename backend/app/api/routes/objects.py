from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_container
from app.models.common import ApiResponse, SourceInfo
from app.services.helpers import build_freshness, utc_now
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/objects", tags=["objects"])


@router.get("/live")
async def live_objects(container: ServiceContainer = Depends(get_container)) -> ApiResponse[dict[str, object]]:
    orbit = await container.orbit_service.get_overview()
    solar = await container.solar_system_service.list_bodies()
    neo = await container.neo_service.get_feed()
    deep_space = await container.deep_space_service.list_objects()
    updated_at = utc_now()
    return ApiResponse(
        status="ok",
        freshness=build_freshness(classification="refreshed", updated_at=updated_at),
        warnings=orbit.warnings + neo.warnings,
        sources=[
            SourceInfo(
                provider="aggregated-discovery",
                dataset="cross-mode live objects",
                classification="refreshed",
                status="ok",
                fetched_at=updated_at,
            )
        ],
        data={
            "featured_orbit": orbit.data.featured,
            "solar_highlights": solar.data[:6],
            "neo_watch": neo.data[:6],
            "deep_space_highlights": deep_space.data[:6],
        },
    )
