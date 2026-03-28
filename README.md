# Universe Visualizer

Universe Visualizer is a premium observatory-style web application for exploring Earth orbit, the Solar System, near-Earth objects, and curated deep-space content from one interface. ISS tracking is included, but it is deliberately one feature inside a broader live-data-driven space visualization platform.

## What Is Included
- React + TypeScript + Vite frontend with CesiumJS as the primary 3D engine
- FastAPI backend with normalized response envelopes, provider health reporting, cache-backed services, and demo-mode fallback
- Earth Orbit, Solar System, NEO, Deep Space, and Featured Tours modes
- Universal search, favorites/watchlist, APOD content, and guided discovery flows
- Documented multi-agent workflow under [AGENT_WORKFLOW.md](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/AGENT_WORKFLOW.md) and [agents/](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/agents)

## Project Structure
- [frontend](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/frontend): React/Cesium client
- [backend](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/backend): FastAPI API and data services
- [agents](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/agents): multi-agent role definitions and shared communication log
- [plans](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/plans): high-level implementation blueprint
- [research](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/research): provider, astronomy, and visualization research notes

## Live Data Strategy
- Orbit mode uses propagated public orbital element data when the live path is available.
- NEO and APOD routes can use NASA APIs.
- Solar System mode currently uses a built-in orbital model for a stable v1 heliocentric scene.
- Deep Space mode is intentionally cataloged and curated, not marketed as live telemetry.
- Demo fallback exists for every domain so the observatory remains usable even when live providers fail.

## Setup
- Frontend guide: [frontend/SETUP.md](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/frontend/SETUP.md)
- Backend guide: [backend/SETUP.md](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/backend/SETUP.md)
- Shared environment example: [.env.example](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/.env.example)

## Verification
- Backend syntax check: `python -m compileall app`
- Backend tests: `python -m unittest discover tests`
- Frontend build verification requires installing the Node dependencies first

## Multi-Agent Workflow
The agent framework is operational rather than decorative:
- each required logical agent has a dedicated markdown contract in [agents](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/agents)
- shared decisions and handoffs are tracked in [agents/communication.md](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/agents/communication.md)
- phase order, implementation gates, and review checkpoints are defined in [AGENT_WORKFLOW.md](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/AGENT_WORKFLOW.md)
