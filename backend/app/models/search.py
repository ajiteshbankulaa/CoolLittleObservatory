from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    id: str
    name: str
    mode: Literal["earth-orbit", "solar-system", "neo", "deep-space", "featured-tour"]
    category: str
    summary: str
    tags: list[str] = Field(default_factory=list)
    freshness_label: str
