from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="Universe Visualizer API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    api_prefix: str = Field(default="/api", alias="API_PREFIX")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    frontend_origin: str = Field(
        default="http://localhost:5173",
        alias="FRONTEND_ORIGIN",
    )

    universe_demo_mode: bool = Field(default=False, alias="UNIVERSE_DEMO_MODE")
    enable_live_providers: bool = Field(default=True, alias="ENABLE_LIVE_PROVIDERS")
    request_timeout_seconds: float = Field(
        default=10.0,
        alias="REQUEST_TIMEOUT_SECONDS",
    )

    orbit_cache_ttl_seconds: int = Field(default=300, alias="ORBIT_CACHE_TTL_SECONDS")
    neo_cache_ttl_seconds: int = Field(default=1800, alias="NEO_CACHE_TTL_SECONDS")
    solar_cache_ttl_seconds: int = Field(default=21600, alias="SOLAR_CACHE_TTL_SECONDS")
    deep_space_cache_ttl_seconds: int = Field(
        default=86400,
        alias="DEEP_SPACE_CACHE_TTL_SECONDS",
    )
    content_cache_ttl_seconds: int = Field(
        default=21600,
        alias="CONTENT_CACHE_TTL_SECONDS",
    )
    active_satellite_limit: int = Field(default=60, alias="ACTIVE_SATELLITE_LIMIT")
    orbit_prediction_steps: int = Field(default=18, alias="ORBIT_PREDICTION_STEPS")
    orbit_prediction_step_minutes: int = Field(
        default=10,
        alias="ORBIT_PREDICTION_STEP_MINUTES",
    )

    nasa_api_key: str = Field(default="DEMO_KEY", alias="NASA_API_KEY")
    nasa_api_base: str = Field(
        default="https://api.nasa.gov",
        alias="NASA_API_BASE",
    )
    celestrak_base: str = Field(
        default="https://celestrak.org/NORAD/elements",
        alias="CELESTRAK_BASE",
    )
    jpl_horizons_base: str = Field(
        default="https://ssd.jpl.nasa.gov/api/horizons.api",
        alias="JPL_HORIZONS_BASE",
    )

    refresh_orbit_seconds: int = Field(default=300, alias="REFRESH_ORBIT_SECONDS")
    refresh_neo_seconds: int = Field(default=1800, alias="REFRESH_NEO_SECONDS")
    refresh_solar_seconds: int = Field(default=21600, alias="REFRESH_SOLAR_SECONDS")
    refresh_deep_space_seconds: int = Field(
        default=86400,
        alias="REFRESH_DEEP_SPACE_SECONDS",
    )
    refresh_content_seconds: int = Field(
        default=21600,
        alias="REFRESH_CONTENT_SECONDS",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

