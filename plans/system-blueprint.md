# Universe Visualizer System Blueprint

## Summary
- Product shape: premium observatory web app with five major modes
- Core stack: React + TypeScript + Vite + TanStack Query + CesiumJS, backed by FastAPI
- Contract rule: backend exposes normalized, provider-agnostic responses with freshness and provenance
- Trust rule: orbit and time-sensitive events are near-live; deep-space content is curated or refreshed

## Mode Map
- `Earth Orbit`: near-live orbital assets, ISS, stations, representative satellites, ground tracks, follow mode, timeline
- `Solar System`: interactive Sun-centered scene with planets, notable moons, scale presets, and detail panels
- `Asteroids / NEOs`: close-approach feed, hazard and size filters, timeline and approach framing
- `Deep Space`: curated stars, clusters, nebulae, compact objects, exoplanet systems, and Milky Way context
- `Featured Tours`: guided scene presets, editorial highlights, and “interesting now” entry points

## Contract Principles
- Every API response returns `status`, `freshness`, `warnings`, `sources`, and `data`
- Every object detail view gets source type, freshness classification, and key metrics
- Demo data uses the same contracts as live data and is visibly marked through warnings and source metadata

## Engineering Principles
- CesiumJS is the primary visualization engine for all modes
- Backend routes stay provider-agnostic and normalization happens server-side
- Frontend keeps Cesium long-lived and imperatively updated while React manages UI overlays
- Search, featured tours, and favorites bridge all major modes
