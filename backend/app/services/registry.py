from __future__ import annotations

import asyncio
import contextlib
from dataclasses import dataclass

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.providers.demo import DemoDataProvider
from app.providers.nasa import NasaProvider
from app.providers.orbit import CelesTrakOrbitProvider
from app.services.content import ContentService
from app.services.deep_space import DeepSpaceService
from app.services.featured import FeaturedService
from app.services.health import HealthService
from app.services.neo import NeoService
from app.services.orbit import OrbitService
from app.services.search import SearchService
from app.services.solar_system import SolarSystemService


class RefreshCoordinator:
    def __init__(self) -> None:
        self._tasks: list[asyncio.Task[None]] = []
        self._stopped = asyncio.Event()

    async def start(self, jobs: list[tuple[str, int, object]]) -> None:
        self._stopped.clear()
        for name, interval, callback in jobs:
            self._tasks.append(asyncio.create_task(self._runner(name, interval, callback)))

    async def _runner(self, name: str, interval: int, callback: object) -> None:
        await callback()
        while not self._stopped.is_set():
            try:
                await asyncio.wait_for(self._stopped.wait(), timeout=interval)
            except TimeoutError:
                await callback()

    async def stop(self) -> None:
        self._stopped.set()
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self._tasks.clear()


@dataclass
class ServiceContainer:
    orbit_service: OrbitService
    solar_system_service: SolarSystemService
    neo_service: NeoService
    deep_space_service: DeepSpaceService
    content_service: ContentService
    featured_service: FeaturedService
    search_service: SearchService
    health_service: HealthService
    refresh_coordinator: RefreshCoordinator
    settings: Settings

    async def start(self) -> None:
        await self.refresh_coordinator.start(
            [
                ("orbit", self.settings.refresh_orbit_seconds, self.orbit_service.prefetch),
                ("solar", self.settings.refresh_solar_seconds, self.solar_system_service.prefetch),
                ("neo", self.settings.refresh_neo_seconds, self.neo_service.prefetch),
                ("deep-space", self.settings.refresh_deep_space_seconds, self.deep_space_service.prefetch),
                ("content", self.settings.refresh_content_seconds, self.content_service.prefetch),
            ]
        )

    async def stop(self) -> None:
        await self.refresh_coordinator.stop()


def build_container(settings: Settings) -> ServiceContainer:
    cache = AsyncTTLCache()
    orbit_live = CelesTrakOrbitProvider(settings)
    orbit_demo = DemoDataProvider("orbit")
    solar_demo = DemoDataProvider("solar-system")
    neo_demo = DemoDataProvider("neo")
    deep_space_demo = DemoDataProvider("deep-space")
    content_demo = DemoDataProvider("content")
    featured_demo = DemoDataProvider("featured")
    nasa = NasaProvider(settings)

    orbit_service = OrbitService(settings, cache, orbit_live, orbit_demo)
    solar_system_service = SolarSystemService(settings, cache, solar_demo)
    neo_service = NeoService(settings, cache, nasa, neo_demo)
    deep_space_service = DeepSpaceService(settings, cache, deep_space_demo)
    content_service = ContentService(settings, cache, nasa, content_demo)
    featured_service = FeaturedService(featured_demo)
    search_service = SearchService(
        orbit_service,
        solar_system_service,
        neo_service,
        deep_space_service,
        featured_service,
    )
    health_service = HealthService(
        [
            orbit_live,
            orbit_demo,
            solar_demo,
            neo_demo,
            deep_space_demo,
            content_demo,
            featured_demo,
            nasa,
        ]
    )

    return ServiceContainer(
        orbit_service=orbit_service,
        solar_system_service=solar_system_service,
        neo_service=neo_service,
        deep_space_service=deep_space_service,
        content_service=content_service,
        featured_service=featured_service,
        search_service=search_service,
        health_service=health_service,
        refresh_coordinator=RefreshCoordinator(),
        settings=settings,
    )
