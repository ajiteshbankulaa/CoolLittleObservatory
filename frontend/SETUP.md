# Frontend Setup

## Prerequisites
- Node.js 20 or newer
- npm 10 or newer

## Install
1. Open a terminal in [frontend](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/frontend).
2. Copy the environment example:
   PowerShell: `Copy-Item .env.example .env`
3. Install dependencies:
   `npm install`

## Run
1. Start the dev server:
   `npm run dev`
2. Open:
   [http://localhost:5173](http://localhost:5173)

## Build
- Production build:
  `npm run build`
- Local preview:
  `npm run preview`

## Notes
- `VITE_API_BASE_URL` should point at the FastAPI backend, typically `http://localhost:8000/api`.
- The frontend expects the backend’s normalized response envelopes and demo fallback behavior.
- Cesium assets are copied during the Vite build through `vite-plugin-static-copy`.
