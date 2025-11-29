# Backend Directory Structure

## 📁 Current Structure

```
backend/
├── app/                      # Main application package
│   ├── __init__.py          # Flask app factory
│   ├── api/                 # API endpoints (blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── patients.py      # Patient CRUD endpoints
│   │   ├── doctors.py       # Doctor CRUD endpoints
│   │   ├── diagnosis.py     # Diagnosis & ML prediction endpoints
│   │   ├── drugs.py         # Drug search endpoints
│   │   ├── prescriptions.py # Prescription endpoints
│   │   └── appointments.py  # Appointment endpoints
│   ├── models/              # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── patient.py       # Patient model
│   │   ├── doctor.py        # Doctor model
│   │   ├── diagnosis.py     # Diagnosis model
│   │   ├── prescription.py  # Prescription model
│   │   ├── appointment.py   # Appointment model
│   │   ├── drug.py          # Drug model
│   │   ├── disease.py       # Disease model
│   │   └── symptom.py       # Symptom model
│   └── utils/               # Utility services
│       ├── __init__.py
│       ├── ml_service.py    # ML model prediction service
│       └── drugbank_service.py  # DrugBank database service
├── tests/                    # Test suite (ready for tests)
│   ├── __init__.py
│   └── README.md
├── config.py                 # Configuration classes
├── run.py                    # Development server entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Backend documentation
```

## ✅ Correct Structure

All application code is in `backend/app/` following Flask's application factory pattern:
- `app/` - Main application package
- `app/api/` - API endpoints
- `app/models/` - Database models
- `app/utils/` - Utility services

## ❌ Removed Empty Folders

The following empty folders were removed (they were leftovers from initial planning):
- ~~`backend/api/`~~ - Empty, removed
- ~~`backend/config/`~~ - Empty, removed  
- ~~`backend/models/`~~ - Empty, removed
- ~~`backend/utils/`~~ - Empty, removed

All functionality is properly organized in `backend/app/` subdirectories.

## 📝 Tests Folder

The `tests/` folder is set up and ready for test development:
- `__init__.py` - Package marker
- `README.md` - Test documentation

You can start adding tests here when ready:
```
tests/
├── test_models/
├── test_api/
└── test_utils/
```

## 🔧 Key Files

### Entry Point
- `run.py` - Starts the Flask development server

### Configuration
- `config.py` - Development/Production/Testing configurations

### Application Factory
- `app/__init__.py` - Creates and configures the Flask app

### API Endpoints
- `app/api/*.py` - All API route handlers

### Database Models
- `app/models/*.py` - All SQLAlchemy database models

### Services
- `app/utils/ml_service.py` - ML prediction service
- `app/utils/drugbank_service.py` - DrugBank data service

## 📦 Dependencies

All Python dependencies are listed in `requirements.txt`.

## 🚀 Running the Backend

```bash
cd backend
python run.py
```

The server will start on `http://localhost:5000`

