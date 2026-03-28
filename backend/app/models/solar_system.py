from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Vector3(BaseModel):
    x: float
    y: float
    z: float


class SolarBody(BaseModel):
    id: str
    name: str
    kind: Literal["star", "planet", "moon", "dwarf-planet"]
    description: str
    color: str
    radius_km: float
    semi_major_axis_au: float
    orbital_period_days: float | None = None
    position_au: Vector3
    orbit_path_au: list[Vector3] = Field(default_factory=list)
    parent_id: str | None = None
    gravity_mps2: float | None = None
    tags: list[str] = Field(default_factory=list)

