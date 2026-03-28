from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/content", tags=["content"])


@router.get("/apod")
async def get_apod(container: ServiceContainer = Depends(get_container)):
    return await container.content_service.get_apod()
