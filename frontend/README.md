# ExoAI Dashboard

Single-page React interface to monitor predictions, inspect light-curve visuals, and review AI-generated evidence.

## Stack
- Vite + React 18 + TypeScript
- Plotly for visual analytics
- Axios for API communication

## Quick start
```bash
cd app/frontend
npm install
npm run dev -- --open
```

The dev server proxies `/api` calls to `http://localhost:8000`. Ensure the FastAPI backend is running and expose a JWT via local storage (e.g., run `localStorage.setItem('EXOAI_TOKEN', 'Bearer <token>')` in the browser console).

## Expected API endpoints
- `GET /api/predictions/candidates` — list latest processed targets.
- `GET /api/predictions/explain?path=...&return_series=true` — returns evidence object with `answer`, `documents`, and `series` arrays.
- `POST /api/predictions/predict` — file upload (exposed optionally in UI for citizen scientists).

## Next steps
- Add login form issuing JWT via dedicated `/auth/token` endpoint when available.
- Include attention overlay heatmap once backend exposes attention arrays per timestamp.
- Hook websocket feed for `stream` endpoint once implemented.
