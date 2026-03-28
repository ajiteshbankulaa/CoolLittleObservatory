from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ApodEntry(BaseModel):
    date: str
    title: str
    explanation: str
    media_type: Literal["image", "video"]
    url: str
    hdurl: str | None = None
    copyright: str | None = None


class TourStop(BaseModel):
    object_id: str | None = None
    mode: Literal["earth-orbit", "solar-system", "neo", "deep-space"]
    title: str
    narrative: str
    camera_hint: str | None = None


class FeaturedTour(BaseModel):
    id: str
    title: str
    summary: str
    duration_minutes: int
    tags: list[str] = Field(default_factory=list)
    stops: list[TourStop] = Field(default_factory=list)

