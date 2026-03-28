from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx
from typing import Any

try:
    from sgp4.api import Satrec, jday
    from sgp4.conveniences import sat_epoch_datetime
except ImportError:  # pragma: no cover - optional runtime dependency
    Satrec = Any  # type: ignore[assignment]
    jday = None
    sat_epoch_datetime = None

from app.core.config import Settings
from app.models.orbit import OrbitPoint
from app.providers.base import BaseProvider


EARTH_RADIUS_KM = 6378.137
EARTH_ECCENTRICITY_SQUARED = 6.69437999014e-3


@dataclass(slots=True)
class TleRecord:
    object_id: str
    name: str
    line1: str
    line2: str
    group: str
    satrec: Satrec
    norad_id: int | None


def parse_tle_stream(payload: str, group: str) -> list[TleRecord]:
    if jday is None:
        raise RuntimeError("sgp4 is required for live orbit propagation")
    lines = [line.strip() for line in payload.splitlines() if line.strip()]
    records: list[TleRecord] = []
    for index in range(0, len(lines), 3):
        chunk = lines[index : index + 3]
        if len(chunk) < 3:
            continue
        name, line1, line2 = chunk
        sat = Satrec.twoline2rv(line1, line2)
        norad_id = None
        try:
            norad_id = int(line1[2:7].strip())
        except ValueError:
            norad_id = None
        object_id = f"orbit-{group}-{norad_id or name.lower().replace(' ', '-')}"
        records.append(
            TleRecord(
                object_id=object_id,
                name=name.title(),
                line1=line1,
                line2=line2,
                group=group,
                satrec=sat,
                norad_id=norad_id,
            )
        )
    return records


def _gmst(jd_value: float) -> float:
    t = (jd_value - 2451545.0) / 36525.0
    gmst_deg = (
        280.46061837
        + 360.98564736629 * (jd_value - 2451545.0)
        + 0.000387933 * t * t
        - (t * t * t) / 38710000.0
    )
    return math.radians(gmst_deg % 360.0)


def _eci_to_geodetic(position_km: tuple[float, float, float], jd_value: float) -> tuple[float, float, float]:
    theta = _gmst(jd_value)
    x_eci, y_eci, z_eci = position_km
    x = x_eci * math.cos(theta) + y_eci * math.sin(theta)
    y = -x_eci * math.sin(theta) + y_eci * math.cos(theta)
    z = z_eci

    longitude = math.atan2(y, x)
    r = math.sqrt(x * x + y * y)
    latitude = math.atan2(z, r)

    for _ in range(5):
        sin_lat = math.sin(latitude)
        c = 1.0 / math.sqrt(1.0 - EARTH_ECCENTRICITY_SQUARED * sin_lat * sin_lat)
        latitude = math.atan2(z + EARTH_RADIUS_KM * c * EARTH_ECCENTRICITY_SQUARED * sin_lat, r)

    sin_lat = math.sin(latitude)
    c = 1.0 / math.sqrt(1.0 - EARTH_ECCENTRICITY_SQUARED * sin_lat * sin_lat)
    altitude = r / math.cos(latitude) - EARTH_RADIUS_KM * c

    return math.degrees(latitude), ((math.degrees(longitude) + 540.0) % 360.0) - 180.0, altitude


def propagate_record(record: TleRecord, at: datetime) -> OrbitPoint:
    if jday is None:
        raise RuntimeError("sgp4 is required for live orbit propagation")
    instant = at.astimezone(timezone.utc)
    second_fraction = instant.second + instant.microsecond / 1_000_000
    jd, fraction = jday(
        instant.year,
        instant.month,
        instant.day,
        instant.hour,
        instant.minute,
        second_fraction,
    )
    error_code, position, velocity = record.satrec.sgp4(jd, fraction)
    if error_code != 0:
        raise RuntimeError(f"SGP4 propagation failed with code {error_code}")

    latitude, longitude, altitude = _eci_to_geodetic(tuple(position), jd + fraction)
    speed = math.sqrt(sum(component * component for component in velocity))

    return OrbitPoint(
        timestamp=instant,
        latitude=latitude,
        longitude=longitude,
        altitude_km=altitude,
        speed_kps=speed,
    )


def record_epoch(record: TleRecord) -> datetime | None:
    if sat_epoch_datetime is None:
        return None
    return sat_epoch_datetime(record.satrec)


class CelesTrakOrbitProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(provider="celestrak", domain="orbit")
        self._settings = settings

    async def fetch_group(self, group: str) -> list[TleRecord]:
        timeout = httpx.Timeout(self._settings.request_timeout_seconds)
        url = f"{self._settings.celestrak_base}/gp.php?GROUP={group}&FORMAT=tle"
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    records = parse_tle_stream(response.text, group)
                    self.record_success(f"Fetched orbit group '{group}' with {len(records)} records.")
                    return records
            except Exception as exc:
                last_error = exc
                if attempt == 2:
                    break
        if last_error is not None:
            self.record_failure(f"Orbit group fetch failed: {last_error}")
            raise last_error
        raise RuntimeError(f"Orbit fetch failed for group '{group}'")
