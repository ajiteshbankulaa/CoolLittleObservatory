from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class CacheEntry(Generic[T]):
    value: T
    expires_at: datetime
    stored_at: datetime

    @property
    def expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at


class AsyncTTLCache:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._store: dict[str, CacheEntry[object]] = {}

    async def get(self, key: str) -> CacheEntry[object] | None:
        async with self._lock:
            return self._store.get(key)

    async def set(self, key: str, value: object, ttl_seconds: int) -> CacheEntry[object]:
        now = datetime.now(timezone.utc)
        entry = CacheEntry(
            value=value,
            stored_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
        )
        async with self._lock:
            self._store[key] = entry
        return entry

    async def pop(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

