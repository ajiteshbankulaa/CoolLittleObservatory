from __future__ import annotations

from datetime import datetime
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field


FreshnessClass = Literal["near-live", "refreshed", "curated", "demo"]
ResponseStatus = Literal["ok", "degraded", "demo"]


class WarningInfo(BaseModel):
    code: str
    message: str
    severity: Literal["info", "warning", "error"] = "warning"


class SourceInfo(BaseModel):
    provider: str
    dataset: str
    classification: FreshnessClass
    status: Literal["ok", "fallback", "demo", "unavailable"] = "ok"
    fetched_at: datetime | None = None
    epoch: datetime | None = None
    url: str | None = None


class FreshnessInfo(BaseModel):
    classification: FreshnessClass
    label: str
    updated_at: datetime
    expires_at: datetime | None = None
    age_seconds: int | None = None


class ProviderHealth(BaseModel):
    provider: str
    domain: str
    status: Literal["healthy", "degraded", "offline", "demo", "unconfigured"]
    message: str | None = None
    last_success: datetime | None = None
    last_failure: datetime | None = None
    last_checked: datetime | None = None


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    status: ResponseStatus
    freshness: FreshnessInfo
    warnings: list[WarningInfo] = Field(default_factory=list)
    sources: list[SourceInfo] = Field(default_factory=list)
    data: T

