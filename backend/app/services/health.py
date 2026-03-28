from __future__ import annotations

from app.models.common import ApiResponse, ProviderHealth, SourceInfo
from app.services.helpers import build_freshness, utc_now


class HealthService:
    def __init__(self, providers: list[object]) -> None:
        self._providers = providers

    async def provider_health(self) -> ApiResponse[list[ProviderHealth]]:
        updated_at = utc_now()
        snapshots = [provider.snapshot() for provider in self._providers]
        return ApiResponse(
            status="ok",
            freshness=build_freshness(classification="refreshed", updated_at=updated_at),
            warnings=[],
            sources=[
                SourceInfo(
                    provider="internal-health",
                    dataset="provider runtime status",
                    classification="refreshed",
                    status="ok",
                    fetched_at=updated_at,
                )
            ],
            data=snapshots,
        )
