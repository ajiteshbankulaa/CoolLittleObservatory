import unittest

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.providers.demo import DemoDataProvider
from app.providers.orbit import CelesTrakOrbitProvider
from app.services.orbit import OrbitService


class OrbitDemoTests(unittest.IsolatedAsyncioTestCase):
    async def test_demo_overview_contains_iss(self):
        settings = Settings()
        settings.universe_demo_mode = True
        settings.enable_live_providers = False

        service = OrbitService(
          settings=settings,
          cache=AsyncTTLCache(),
          live_provider=CelesTrakOrbitProvider(settings),
          demo_provider=DemoDataProvider("orbit"),
        )

        response = await service.get_overview()

        self.assertEqual(response.status, "demo")
        self.assertTrue(any(item.norad_id == 25544 for item in response.data.featured))


if __name__ == "__main__":
    unittest.main()
