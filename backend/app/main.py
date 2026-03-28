from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import content, deep_space, featured, health, neo, objects, orbit, search, solar_system
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.registry import build_container


settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = build_container(settings)
    app.state.container = container
    await container.start()
    yield
    await container.stop()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend API for the Universe Visualizer observatory platform.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(objects.router, prefix=settings.api_prefix)
app.include_router(orbit.router, prefix=settings.api_prefix)
app.include_router(solar_system.router, prefix=settings.api_prefix)
app.include_router(neo.router, prefix=settings.api_prefix)
app.include_router(deep_space.router, prefix=settings.api_prefix)
app.include_router(featured.router, prefix=settings.api_prefix)
app.include_router(content.router, prefix=settings.api_prefix)
app.include_router(search.router, prefix=settings.api_prefix)
app.include_router(health.router, prefix=settings.api_prefix)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }
