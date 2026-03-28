from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search(
    query: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=25),
    container: ServiceContainer = Depends(get_container),
):
    return await container.search_service.search(query=query, limit=limit)
