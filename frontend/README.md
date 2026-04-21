# Frontend (React + Vite)

Patient and doctor dashboards; JWT auth via `src/context/AuthContext.jsx` and `src/services/api.js`.

## Run

```bash
npm install
npm run dev
```

Dev server: **http://localhost:3000**. Requests to **`/api`** are proxied to the Flask backend (**http://localhost:5000**) — see `vite.config.js`.

## Where to read more

**[docs/PROJECT_GUIDE.md](../docs/PROJECT_GUIDE.md)** — full stack wiring, env vars, and ML behavior.

## Main files

| Path | Role |
|------|------|
| `src/main.jsx` | React mount + `BrowserRouter` |
| `src/App.jsx` | Routes, `ProtectedRoute`, role checks |
| `src/services/api.js` | Axios instance, JWT headers, refresh on 401 |
| `src/pages/DoctorDashboard.jsx` | Doctor flows including diagnosis |
| `src/pages/PatientDashboard.jsx` | Patient flows |
