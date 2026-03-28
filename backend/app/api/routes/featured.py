from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/featured", tags=["featured"])


@router.get("/tours")
async def list_tours(container: ServiceContainer = Depends(get_container)):
    return await container.featured_service.list_tours()
