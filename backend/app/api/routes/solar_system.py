from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/solar-system", tags=["solar-system"])


@router.get("/bodies")
async def list_bodies(container: ServiceContainer = Depends(get_container)):
    return await container.solar_system_service.list_bodies()


@router.get("/body/{body_id}")
async def get_body(body_id: str, container: ServiceContainer = Depends(get_container)):
    try:
        return await container.solar_system_service.get_body(body_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Solar-system body '{body_id}' not found") from exc
