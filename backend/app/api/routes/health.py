from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_container
from app.models.common import ApiResponse, SourceInfo
from app.services.helpers import build_freshness, utc_now
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def healthcheck(container: ServiceContainer = Depends(get_container)) -> ApiResponse[dict[str, str]]:
    updated_at = utc_now()
    return ApiResponse(
        status="ok",
        freshness=build_freshness(classification="refreshed", updated_at=updated_at),
        warnings=[],
        sources=[
            SourceInfo(
                provider="internal-health",
                dataset="service heartbeat",
                classification="refreshed",
                status="ok",
                fetched_at=updated_at,
            )
        ],
        data={"status": "ok", "app": container.settings.app_name},
    )


@router.get("/providers")
async def provider_health(container: ServiceContainer = Depends(get_container)):
    return await container.health_service.provider_health()
