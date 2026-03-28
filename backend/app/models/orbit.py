from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


OrbitCategory = Literal["station", "science", "weather", "communication", "satellite"]


class OrbitPoint(BaseModel):
    timestamp: datetime
    latitude: float
    longitude: float
    altitude_km: float
    speed_kps: float


class OrbitObject(BaseModel):
    id: str
    name: str
    norad_id: int | None = None
    category: OrbitCategory
    subcategory: str | None = None
    description: str
    operator: str | None = None
    country: str | None = None
    tags: list[str] = Field(default_factory=list)
    latitude: float
    longitude: float
    altitude_km: float
    speed_kps: float
    inclination_deg: float | None = None
    period_minutes: float | None = None
    tle_epoch: datetime | None = None
    trail: list[OrbitPoint] = Field(default_factory=list)
    ground_track: list[OrbitPoint] = Field(default_factory=list)
    visibility: str | None = None
    tracked: bool = False


class OrbitOverview(BaseModel):
    featured: list[OrbitObject]
    stations: list[OrbitObject]
    satellites: list[OrbitObject]

