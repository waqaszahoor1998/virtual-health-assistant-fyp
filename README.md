# Virtual Health Assistant

Web application for virtual health workflows: JWT auth, patient/doctor dashboards, appointments, prescriptions, drug lookup from a local CSV, and **machine-learned disease suggestions** from symptoms (multi-label; **not** a clinical product).

## Documentation (start here)

**[docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)** — **start here for students:** how to run the project, **current project status**, **file-by-file** descriptions of backend `app/*.py`, frontend `src/*`, and ML scripts, plus how those pieces connect. Treat it as the **canonical** project document.

## Quick run (local)

**1. Backend** (from `backend/`):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

**2. Frontend** (from `frontend/`):

```powershell
npm install
npm run dev
```

- Frontend: **http://localhost:3000** (Vite proxies `/api` → **http://localhost:5000**)
- Seed demo users: `flask seed-db` (run inside `backend/` with venv active; password in `backend/app/cli/seed.py`)
- Build symptom/disease catalogs: `flask build-catalog` (recommended; enables large symptom list in UI)

**ML:** The API expects `ml_models/models/lightgbm_model.pkl` (generate with `ml_models/scripts/feature_engineering.py` then `train_lightgbm.py`). For a UI demo without that file, set `DEMO_ML_FALLBACK=1` in `backend/.env` (see guide).

## Repository map

| Path | Role |
|------|------|
| `backend/` | Flask API, SQLAlchemy models, JWT, `ml_service`, DrugBank CSV service |
| `frontend/` | React + Vite SPA, calls `/api` |
| `ml_models/` | Training scripts and `.pkl` / metrics artifacts |
| `data/` | Processed datasets and `raw/drugbank_clean.csv` (default drug data) |

## License / disclaimer

Educational use. Predictions and drug information must not replace professional medical judgment.
