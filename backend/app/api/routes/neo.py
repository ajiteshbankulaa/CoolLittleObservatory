from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/neo", tags=["neo"])


@router.get("/feed")
async def get_feed(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    container: ServiceContainer = Depends(get_container),
):
    return await container.neo_service.get_feed(start=start, end=end)
