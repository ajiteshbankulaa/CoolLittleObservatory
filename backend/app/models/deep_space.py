from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.models.solar_system import Vector3


class DeepSpaceObject(BaseModel):
    id: str
    name: str
    category: Literal[
        "nearby-star",
        "nebula",
        "star-cluster",
        "compact-object",
        "exoplanet-system",
        "galactic-context",
    ]
    constellation: str | None = None
    distance_ly: float | None = None
    right_ascension_deg: float | None = None
    declination_deg: float | None = None
    galactic_position: Vector3 | None = None
    description: str
    tags: list[str] = Field(default_factory=list)

