# Backend (Flask API)

REST API for the Virtual Health Assistant. Routes live under **`/api`** (see `app/api/`).

## Setup

See the repo **[docs/PROJECT_GUIDE.md](../docs/PROJECT_GUIDE.md)** for:

- `DATABASE_URL`, JWT secrets, `CORS_ORIGINS`, `DEMO_ML_FALLBACK`, `DRUGBANK_CSV`
- Commands: `python run.py`, `flask seed-demo`
- How `ml_service` and `drugbank_service` connect to routes

## Entry points

| File | Purpose |
|------|---------|
| `run.py` | Loads `.env`, builds app via `create_app()`, runs dev server |
| `config.py` | `DevelopmentConfig` / `ProductionConfig` / `TestingConfig` |
| `app/__init__.py` | App factory, extensions, blueprint registration |
| `app/cli/seed.py` | `flask seed-demo` — demo users and records |
