from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models.common import FreshnessClass, FreshnessInfo


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def build_freshness(
    classification: FreshnessClass,
    updated_at: datetime,
    ttl_seconds: int | None = None,
) -> FreshnessInfo:
    expires_at = updated_at + timedelta(seconds=ttl_seconds) if ttl_seconds else None
    age_seconds = int((utc_now() - updated_at).total_seconds())
    label = {
        "near-live": "Near-live propagated state",
        "refreshed": "Refreshed scientific dataset",
        "curated": "Curated astronomy catalog",
        "demo": "Demo fallback dataset",
    }[classification]
    return FreshnessInfo(
        classification=classification,
        label=label,
        updated_at=updated_at,
        expires_at=expires_at,
        age_seconds=max(age_seconds, 0),
    )
