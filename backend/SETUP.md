# Backend Setup

## Prerequisites
- Python 3.11 or newer
- `pip`

## Install
1. Open a terminal in [backend](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/backend).
2. Create a virtual environment:
   `python -m venv .venv`
3. Activate it:
   PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   `pip install -e .`
5. Copy the environment example:
   PowerShell: `Copy-Item .env.example .env`

## Run
1. Start the API:
   `uvicorn app.main:app --reload`
2. Open the docs:
   [http://localhost:8000/docs](http://localhost:8000/docs)

## Test
- Syntax check:
  `python -m compileall app`
- Unit tests:
  `python -m unittest discover tests`

## Notes
- `UNIVERSE_DEMO_MODE=true` forces the API to use built-in datasets.
- `ENABLE_LIVE_PROVIDERS=true` enables public live paths where implemented.
- Orbit mode can use public CelesTrak TLE feeds when `sgp4` is installed.
- NASA-backed routes use `NASA_API_KEY`; `DEMO_KEY` works for development with lower quotas.
