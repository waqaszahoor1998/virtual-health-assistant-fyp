# Virtual Health Assistant — Student & Maintainer Guide

This document is the **single source of truth** for how the project is structured today, how the pieces connect, and how to run everything on your PC (Windows-friendly). Older markdown files at the repo root that disagreed with the code have been removed; use this guide instead.

---

## 1. What this project does

- **Web app**: Patients and doctors log in (JWT). Doctors manage patients, appointments, prescriptions, and run **symptom → disease suggestions** using a trained ML pipeline. Patients can view their records and use a **patient-facing** prediction endpoint (informational only).
- **ML**: Symptoms are turned into numbers with the **same TF-IDF vectorizer** used in training, then a **multi-label classifier** predicts scores for many diseases; the API returns the top matches.
- **Drugs**: Drug search uses a **CSV** (DrugBank-style export), not a live DrugBank API.

**Important:** Outputs are **not medical advice**. The UI and API include disclaimers.

---

## 2. Repository layout (how folders link together)

```
rehan/
├── backend/                 # Flask API (Python)
│   ├── run.py               # Start the dev server (loads backend/.env)
│   ├── config.py            # DB URL, JWT, paths to ML + DrugBank CSV
│   ├── app/
│   │   ├── __init__.py      # create_app(): DB, JWT, CORS, registers /api blueprint
│   │   ├── api/             # HTTP routes (auth, patients, diagnosis, drugs, …)
│   │   ├── models/          # SQLAlchemy ORM models (tables)
│   │   ├── utils/
│   │   │   ├── ml_service.py      # Loads .pkl models + vectorizer; predict_diseases()
│   │   │   └── drugbank_service.py # Loads DRUGBANK_CSV; search
│   │   └── cli/seed.py      # flask seed-db (demo users + data)
│   └── .env.example         # Copy to .env for local demo (SQLite, CORS, secrets)
│
├── frontend/                # React (Vite)
│   ├── vite.config.js       # Dev server port 3000; proxies /api → localhost:5000
│   └── src/
│       ├── main.jsx         # React entry
│       ├── App.jsx          # Routes + AuthProvider + role guards
│       ├── context/AuthContext.jsx   # Login, tokens in localStorage
│       └── services/api.js  # Axios: base URL /api, JWT interceptors
│
├── ml_models/
│   ├── scripts/             # feature_engineering.py, train_lightgbm.py, etc.
│   └── models/              # Artifacts: vectorizer, X_*.pkl, *model*.pkl, metrics JSON
│
└── data/
    ├── processed/           # dataset_cleaned.xlsx (and optional expanded files)
    └── raw/                 # drugbank_clean.csv (default for DrugBank service)
```

**Request path (diagnosis example):**

1. Browser calls `POST /api/diagnosis/predict` with JWT (doctor role).
2. `diagnosis.py` validates input → `get_ml_service()` → `MLPredictionService.predict_diseases()`.
3. `ml_service` loads `symptom_vectorizer.pkl` + `lightgbm_model.pkl` (or demo fallback — see below).
4. JSON response returns `predictions`, `model_used`, etc.

---

## 3. Tech stack (current)

| Layer | Technology |
|--------|------------|
| Frontend | React 18, Vite, React Router, Bootstrap, Axios |
| Backend | Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Migrate, Flask-CORS |
| Database | **Local demo:** SQLite (`DATABASE_URL` in `.env`). **Production-style:** PostgreSQL URL in env |
| ML training | Python, scikit-learn, LightGBM (and optional scripts: XGBoost, NN, stacking) |
| ML inference (API) | **Primary:** LightGBM inside `MultiOutputClassifier`. **Optional:** XGBoost / Random Forest if their `.pkl` files exist |

---

## 4. Machine learning — what is actually used in the API

### 4.1 Production inference path

- **File:** `backend/app/utils/ml_service.py`
- **Primary model file:** `ml_models/models/lightgbm_model.pkl`
- **Required companions:** `symptom_vectorizer.pkl`, `disease_encoder.pkl`, `unique_diseases.txt` (and the usual `X_*.pkl` / `y_*.pkl` for **training**, not loaded at API runtime)

**How prediction works:**

1. Symptom strings are joined into one lowercase string (same idea as training).
2. `TfidfVectorizer` produces a sparse/dense feature row.
3. The trained model’s `predict_proba` returns per-label probabilities; the service keeps labels above a small threshold, sorts, returns **top_k**.

### 4.2 Metrics snapshot (from committed JSON, not “marketing” numbers)

- See `ml_models/models/lightgbm_model_metrics.json` and `lightgbm_model_info.json` for the **exact** last recorded test metrics (e.g. F1-micro on the held-out set).
- See `ml_models/models/metadata.json` for **dataset shape** used when those artifacts were built (feature count, label count, split sizes).

Multi-label disease prediction on large label spaces is **hard**; accuracy depends heavily on dataset size and label granularity. Treat metrics as **experimental**, not clinical validation.

### 4.3 Other scripts under `ml_models/scripts/`

Scripts such as `train_xgboost.py`, `train_neural_network.py`, `train_stacking_ensemble.py` are for **research / coursework**. The Flask app does **not** automatically load the stacking or neural network models unless you extend `ml_service.py` to do so.

### 4.4 Demo mode when `lightgbm_model.pkl` is missing

If the main model file is absent and loading fails, setting **`DEMO_ML_FALLBACK=1`** enables a **deterministic keyword + hash** fallback so the UI still returns plausible-looking suggestions for demos. Responses will show `model_used: "demo_fallback"`. This is **not** real ML.

---

## 5. Environment variables (backend)

Copy `backend/.env.example` to `backend/.env` and adjust.

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | e.g. `sqlite:///demo.db` for local SQLite |
| `SECRET_KEY` / `JWT_SECRET_KEY` | Signing sessions/tokens; change for any real deployment |
| `CORS_ORIGINS` | Must include your frontend origin (default example: `http://localhost:3000`) |
| `DRUGBANK_CSV` | Optional override path to `drugbank_clean.csv` |
| `DEMO_ML_FALLBACK` | Set to `1` only for demos without `lightgbm_model.pkl` |
| `FLASK_ENV` | `development` (default) or `production` |
| `PORT` | Backend port (default `5000`) |

`config.py` defines defaults; **development** still expects you to set `DATABASE_URL` for SQLite if you do not run PostgreSQL.

---

## 6. Run on your PC

### 6.1 Prerequisites

- **Python 3.10+** (3.8+ may work; use a venv)
- **Node.js 18+** and npm (for the frontend)

### 6.2 Backend

**Windows (PowerShell):**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Train ML (see §7) or set DEMO_ML_FALLBACK=1 in .env for demo-only predictions
python run.py
```

API base: `http://localhost:5000`  
API routes are under **`/api/...`** (blueprint prefix).

**Seed demo users and records:**

```powershell
flask seed-db
```

Default demo password is in `backend/app/cli/seed.py` (`demo123`).

**Build symptom/disease catalogs (recommended):**

This fills the database tables `symptoms` and `diseases` so the frontend can load
a large symptom list (autocomplete/search) from the backend.

```powershell
flask build-catalog
```

### 6.3 Frontend

```powershell
cd frontend
npm install
npm run dev
```

Vite serves the app at **`http://localhost:3000`** and proxies **`/api`** to port **5000**.

If you deploy the frontend separately, set `VITE_API_BASE_URL` to your backend’s `/api` URL.

---

## 7. Train or refresh ML artifacts

**Order of operations:**

1. Ensure processed data exists, e.g. `data/processed/dataset_cleaned.xlsx` (see `data/scripts/` if you need to regenerate).
2. From repo root:

```powershell
cd ml_models\scripts
python feature_engineering.py
```

3. Train the model the API expects:

```powershell
python train_lightgbm.py
```

This should create **`ml_models/models/lightgbm_model.pkl`** plus metrics/info JSON files.

Optional: run other `train_*.py` scripts for coursework comparisons; only LightGBM (and optionally RF/XGB if present) is wired in `ml_service.py` today.

---

## 8. Authentication (short version)

- **Login** returns JWT **access** and **refresh** tokens.
- The frontend stores them in `localStorage` and attaches `Authorization: Bearer <access>` via `src/services/api.js`.
- **Access** expiry is configured in `backend/config.py` (default 1 hour). **Refresh** is used on 401 to obtain a new access token.
- Role checks: e.g. `POST /api/diagnosis/predict` requires **doctor**; `POST /api/diagnosis/predict-self` requires **patient**.

For deeper behavior, read `backend/app/api/auth.py` and `frontend/src/context/AuthContext.jsx` side by side.

---

## 9. Database tables (conceptual)

ORM models live in `backend/app/models/`. Typical entities:

- **User** — email, password hash, role (`patient` / `doctor`)
- **Patient** / **Doctor** — profile rows linked to `User`
- **Diagnosis** — symptoms + ML output + doctor notes
- **Prescription**, **Appointment**, consultation requests, etc.

In **development**, `create_app` runs `db.create_all()` so SQLite file DBs stay simple. For production, use migrations (`Flask-Migrate`).

---

## 10. Project status (current scope)

Use this as the **honest checklist** of what the repo implements today (not marketing).

| Area | Status |
|------|--------|
| Patient / doctor registration & login (JWT) | Implemented (`auth.py`, `AuthContext.jsx`) |
| Dashboards (appointments, prescriptions, diagnosis flows) | Implemented (`PatientDashboard.jsx`, `DoctorDashboard.jsx`) |
| Symptom → disease API | Implemented; primary model **LightGBM** in `ml_service.py` |
| Drug search from CSV | Implemented (`drugbank_service.py`, `drugs.py`) |
| Demo DB seed | `flask seed-db` (`cli/seed.py`) |
| SQLite local demo | Supported via `DATABASE_URL` in `.env` |
| Optional ML demo without `.pkl` | `DEMO_ML_FALLBACK=1` |
| Extra trainers (NN, stacking, CatBoost, …) | Present under `ml_models/scripts/`; **not** auto-loaded by Flask unless you change `ml_service.py` |

**What students should do first:** run backend + frontend (§6), seed demo users, log in, trace one API call from the browser Network tab to the matching function in `app/api/*.py`.

---

## 11. Backend: what each important `.py` file does

**Entry & configuration**

| File | Role |
|------|------|
| `backend/run.py` | Starts Flask; loads `.env`; calls `create_app()`. |
| `backend/config.py` | `DevelopmentConfig` / `ProductionConfig` / `TestingConfig`: `DATABASE_URL`, JWT expiry, `ML_MODELS_DIR`, `DATA_DIR`, `DRUGBANK_CSV`. |

**Application core**

| File | Role |
|------|------|
| `backend/app/__init__.py` | **App factory:** `db`, `jwt`, `migrate`, CORS, registers `api_bp` at `/api`, `db.create_all()` in development, registers `flask seed-db` and `flask build-catalog`. |
| `backend/app/api/__init__.py` | Defines `api_bp` blueprint; imports route modules so routes attach to the blueprint. |

**HTTP routes (all live under URL prefix `/api`)**

| File | Role |
|------|------|
| `backend/app/api/auth.py` | Register, login, refresh JWT, current user. |
| `backend/app/api/patients.py` | Patient CRUD / listing (as permitted by role). |
| `backend/app/api/doctors.py` | Doctor profiles / listing. |
| `backend/app/api/diagnosis.py` | **ML path:** `predict`, `predict-self`, create/list/get diagnoses. Uses `get_ml_service()`. |
| `backend/app/api/drugs.py` | Drug search endpoints using `DrugBankService`. |
| `backend/app/api/prescriptions.py` | Prescription create/list/update. |
| `backend/app/api/appointments.py` | Appointment scheduling. |
| `backend/app/api/consultations.py` | Consultation requests between patient and doctor flows. |

**Services (shared logic, no HTTP)**

| File | Role |
|------|------|
| `backend/app/utils/ml_service.py` | Loads pickles from `ml_models/models`, vectorizes symptoms, runs `predict_proba`, optional `DEMO_ML_FALLBACK`. |
| `backend/app/utils/drugbank_service.py` | Loads `DRUGBANK_CSV`, filters columns, search helpers. |
| `backend/app/utils/__init__.py` | Package marker (often empty or re-exports). |

**Database (SQLAlchemy models — one file ≈ one or more tables)**

| File | Role |
|------|------|
| `backend/app/models/__init__.py` | Imports all models so SQLAlchemy registers them with `db`. |
| `backend/app/models/user.py` | Users: email, password hash, role. |
| `backend/app/models/patient.py` | Patient profile linked to `User`. |
| `backend/app/models/doctor.py` | Doctor profile linked to `User`. |
| `backend/app/models/diagnosis.py` | Stored diagnosis + symptoms / ML output JSON. |
| `backend/app/models/prescription.py` | Prescriptions. |
| `backend/app/models/appointment.py` | Appointments. |
| `backend/app/models/consultation_request.py` | Consultation requests. |
| `backend/app/models/drug.py`, `disease.py`, `symptom.py` | Catalog-style models (used if your schema/migrations populate them). |

**CLI**

| File | Role |
|------|------|
| `backend/app/cli/seed.py` | `flask seed-db` — creates demo doctor/patients/appointments/diagnoses/prescriptions. |
| `backend/app/cli/catalog.py` | `flask build-catalog` — populates `symptoms` and `diseases` tables from artifacts/data (idempotent). |

**How routes tie to models:** Each `*.py` in `api/` imports `db` and the ORM classes it needs (`User`, `Patient`, …), checks JWT identity and role, then reads/writes rows. **Diagnosis** is special: it also calls `ml_service`, which only reads files under `ml_models/models/`.

---

## 12. Frontend: what each important file does

| File | Role |
|------|------|
| `frontend/src/main.jsx` | Mounts React; wraps app in `BrowserRouter`. |
| `frontend/src/App.jsx` | Route table; `ProtectedRoute` + role checks; layout shell. |
| `frontend/src/context/AuthContext.jsx` | Login/register/logout; stores JWT + user in `localStorage`. |
| `frontend/src/services/api.js` | Axios client to `/api`; attaches Bearer token; refresh on 401. |
| `frontend/src/pages/LoginPage.jsx` | Auth UI. |
| `frontend/src/pages/DoctorDashboard.jsx` | Doctor workflows (patients, diagnosis, prescriptions, etc.). |
| `frontend/src/pages/PatientDashboard.jsx` | Patient workflows (records, booking, optional self-prediction). |
| `frontend/src/pages/NotFound.jsx` | 404 page. |
| `frontend/src/components/SymptomSelector.jsx` | Symptom UI used in diagnosis flows. |
| `frontend/src/components/DiseasePredictionCard.jsx` | Displays ML results. |
| `frontend/src/components/AppointmentBookingModal.jsx` | Appointment UI. |
| `frontend/src/components/layout/Navbar.jsx`, `Footer.jsx` | Chrome. |

**Connection rule:** Pages call `api.get` / `api.post` (from `api.js`). Those hit `http://localhost:5000/api/...` in dev because `vite.config.js` **proxies** `/api` to the backend.

### Catalog endpoints used by the UI

- `GET /api/catalog/symptoms?q=<optional>&page=1&per_page=200` (JWT required)
- `GET /api/catalog/diseases?q=<optional>&page=1&per_page=200` (JWT required)

The doctor diagnosis UI loads symptoms from `/api/catalog/symptoms` on mount and
falls back to a small built-in list if the catalog is empty.

---

## 13. ML folder: what each script does

All under `ml_models/scripts/`; outputs go to `ml_models/models/`.

| Script | Role |
|--------|------|
| `feature_engineering.py` | Reads cleaned dataset from `data/processed/`, fits TF-IDF + label matrix, writes `X_*.pkl`, `y_*.pkl`, `symptom_vectorizer.pkl`, `disease_encoder.pkl`, `metadata.json`, etc. |
| `train_lightgbm.py` | Trains **LightGBM** `MultiOutputClassifier`; writes `lightgbm_model.pkl` + metrics JSON (**this is what the API loads first**). |
| `train_xgboost.py` | Optional; `ml_service` loads if `xgboost_model.pkl` exists. |
| `train_random_forest.py` | Optional; `ml_service` loads if `random_forest_model.pkl` exists. |
| `train_neural_network.py` | Experiment; not wired into Flask by default. |
| `train_catboost.py` | Experiment; not wired into Flask by default. |
| `train_ensemble.py` | Experiment; not wired into Flask by default. |
| `train_stacking_ensemble.py` | Experiment; not wired into Flask by default. |
| `train_all_models.py` | Convenience runner for multiple trainers. |
| `analyze_data.py` | Exploratory / reporting on data. |

### Data preparation (`data/scripts/`)

Used **before** `feature_engineering.py` if you need to rebuild `data/processed/dataset_cleaned.xlsx` or merge downloads.

| Script | Role |
|--------|------|
| `clean_symptoms.py` | Cleans symptom text / builds processed files (see script header). |
| `merge_datasets.py`, `normalize_datasets.py`, `normalize_and_merge_datasets.py` | Combine or normalize sources into a consistent schema. |
| `download_datasets_simple.py`, `download_kaggle_datasets.py`, `download_large_datasets.py`, `download_with_token.py` | Fetch external CSVs/archives. |
| `setup_kaggle.py`, `create_kaggle_json.py` | Kaggle API setup helpers. |

Details vary by script; open each file for exact inputs/outputs. `data/scripts/README.md` may have extra notes.

---

## 14. What changed in documentation (for instructors)

Many old root-level `.md` files **contradicted** each other and the code (different dataset sizes, ports, and commands). They were removed so students do not study the wrong system. **All essential “how to run + how it connects” content belongs in this guide** and in short READMEs that link here. If coursework requires a formal “project plan” document, use **§10** and **§16** below as the template and extend in your LMS — do not resurrect conflicting copies in the repo.

---

## 15. Troubleshooting

| Symptom | Likely cause | What to do |
|---------|----------------|------------|
| CORS errors | Frontend not in `CORS_ORIGINS` | Add `http://localhost:3000` to `.env` |
| 503 “ML models not available” | No `lightgbm_model.pkl` | Run training (§7) or `DEMO_ML_FALLBACK=1` |
| Drug search empty / 500 | Missing CSV | Place `data/raw/drugbank_clean.csv` or set `DRUGBANK_CSV` |
| Wrong API port | Vite proxy targets 5000 | Run backend on 5000 or change `vite.config.js` |
| PostgreSQL connection errors | Default `config.py` example URL | Use SQLite in `.env` for local work |

---

## 16. Suggested project milestones (for students)

Use this as a **planning checklist**, not a guarantee of schedule.

1. Environment + `.env` + run backend/frontend.
2. Trace one authenticated request: `api.js` → Flask route → DB or service.
3. Run `feature_engineering.py` and `train_lightgbm.py`; verify `.pkl` appears.
4. Extend UI or API **in one small vertical slice** (e.g. better symptom picker) before large refactors.

---

*Last aligned with the codebase layout and config described in this repository. If you change inference wiring or ports, update this file in the same PR.*
