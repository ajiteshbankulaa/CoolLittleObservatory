import unittest

from app.core.cache import AsyncTTLCache
from app.core.config import Settings
from app.providers.demo import DemoDataProvider
from app.services.solar_system import SolarSystemService


class SolarSystemServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_solar_bodies_include_moon(self):
        settings = Settings()
        cache = AsyncTTLCache()
        service = SolarSystemService(settings, cache, DemoDataProvider("solar-system"))

        response = await service.list_bodies()
        moon = next(body for body in response.data if body.id == "moon")

        self.assertEqual(response.status, "ok")
        self.assertEqual(moon.parent_id, "earth")
        self.assertGreater(len(moon.orbit_path_au), 10)


if __name__ == "__main__":
    unittest.main()
