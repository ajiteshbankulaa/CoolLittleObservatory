from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_container
from app.services.registry import ServiceContainer


router = APIRouter(prefix="/orbit", tags=["orbit"])


@router.get("/iss")
async def get_iss(container: ServiceContainer = Depends(get_container)):
    try:
        return await container.orbit_service.get_iss()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/stations")
async def get_stations(container: ServiceContainer = Depends(get_container)):
    return await container.orbit_service.get_stations()


@router.get("/satellites")
async def get_satellites(container: ServiceContainer = Depends(get_container)):
    return await container.orbit_service.get_satellites()


@router.get("/object/{object_id}")
async def get_object(object_id: str, container: ServiceContainer = Depends(get_container)):
    try:
        return await container.orbit_service.get_object(object_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Orbit object '{object_id}' not found") from exc


@router.get("/predictions/{object_id}")
async def get_predictions(object_id: str, container: ServiceContainer = Depends(get_container)):
    try:
        return await container.orbit_service.get_predictions(object_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Orbit object '{object_id}' not found") from exc
