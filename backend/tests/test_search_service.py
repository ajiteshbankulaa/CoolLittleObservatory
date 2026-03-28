import unittest

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.providers.demo import DemoDataProvider
from app.providers.nasa import NasaProvider
from app.providers.orbit import CelesTrakOrbitProvider
from app.services.deep_space import DeepSpaceService
from app.services.featured import FeaturedService
from app.services.neo import NeoService
from app.services.orbit import OrbitService
from app.services.search import SearchService
from app.services.solar_system import SolarSystemService


class SearchServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_surfaces_deep_space_object(self):
        settings = Settings()
        settings.universe_demo_mode = True
        settings.enable_live_providers = False
        cache = AsyncTTLCache()

        orbit_service = OrbitService(
            settings=settings,
            cache=cache,
            live_provider=CelesTrakOrbitProvider(settings),
            demo_provider=DemoDataProvider("orbit"),
        )
        solar_service = SolarSystemService(settings, cache, DemoDataProvider("solar-system"))
        neo_service = NeoService(settings, cache, NasaProvider(settings), DemoDataProvider("neo"))
        deep_space_service = DeepSpaceService(settings, cache, DemoDataProvider("deep-space"))
        featured_service = FeaturedService(DemoDataProvider("featured"))
        search_service = SearchService(
            orbit_service=orbit_service,
            solar_system_service=solar_service,
            neo_service=neo_service,
            deep_space_service=deep_space_service,
            featured_service=featured_service,
        )

        response = await search_service.search("Orion")

        self.assertTrue(any(result.id == "orion-nebula" for result in response.data))


if __name__ == "__main__":
    unittest.main()
