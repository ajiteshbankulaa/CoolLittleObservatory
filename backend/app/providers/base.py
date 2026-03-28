from __future__ import annotations

from datetime import datetime, timezone

from app.models.common import ProviderHealth


class BaseProvider:
    def __init__(self, provider: str, domain: str) -> None:
        self.provider = provider
        self.domain = domain
        self._health = ProviderHealth(
            provider=provider,
            domain=domain,
            status="unconfigured",
            last_checked=datetime.now(timezone.utc),
        )

    def record_success(self, message: str | None = None) -> None:
        now = datetime.now(timezone.utc)
        self._health = ProviderHealth(
            provider=self.provider,
            domain=self.domain,
            status="healthy",
            message=message,
            last_success=now,
            last_failure=self._health.last_failure,
            last_checked=now,
        )

    def record_failure(self, message: str) -> None:
        now = datetime.now(timezone.utc)
        self._health = ProviderHealth(
            provider=self.provider,
            domain=self.domain,
            status="degraded",
            message=message,
            last_success=self._health.last_success,
            last_failure=now,
            last_checked=now,
        )

    def mark_demo(self, message: str = "Serving demo dataset.") -> None:
        now = datetime.now(timezone.utc)
        self._health = ProviderHealth(
            provider=self.provider,
            domain=self.domain,
            status="demo",
            message=message,
            last_success=now,
            last_failure=self._health.last_failure,
            last_checked=now,
        )

    def snapshot(self) -> ProviderHealth:
        return self._health

