from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/deep-space", tags=["deep-space"])


@router.get("/objects")
async def list_objects(
    category: str | None = Query(default=None),
    container: ServiceContainer = Depends(get_container),
):
    return await container.deep_space_service.list_objects(category=category)
