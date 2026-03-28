from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.solar_system import Vector3


class NeoObject(BaseModel):
    id: str
    name: str
    designation: str
    is_hazardous: bool
    close_approach: datetime
    miss_distance_km: float
    relative_velocity_kps: float
    estimated_diameter_min_m: float
    estimated_diameter_max_m: float
    orbit_class: str | None = None
    position_au: Vector3 | None = None
    description: str
    tags: list[str] = Field(default_factory=list)

