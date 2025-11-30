# 🏥 Virtual Health Assistant

A comprehensive web application for virtual health assistance with ML-powered disease prediction from symptoms.

## 🎯 Project Overview

- **Frontend:** React + Vite + Bootstrap (modern UI)
- **Backend:** Flask + PostgreSQL + JWT authentication
- **ML Models:** LightGBM (46.31% accuracy) + Neural Network (59.41% F1-Micro)
- **Dataset:** 2,272 training samples, 1,140 diseases, 16,780 drugs

## 🚀 Quick Start

**For complete setup instructions, see:** [`SETUP_AND_GUIDE.md`](./SETUP_AND_GUIDE.md) ⭐

```bash
# Backend (Terminal 1)
cd backend
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
python run.py

# Frontend (Terminal 2)
cd frontend
npm run dev
```

Access at: `http://localhost:5173`

## 📚 Documentation

### Essential Guides
- **[SETUP_AND_GUIDE.md](./SETUP_AND_GUIDE.md)** ⭐ - Complete setup, how code works, user roles, database structure
- **[QUICK_START.md](./QUICK_START.md)** - Fast setup for experienced developers
- **[RUN_COMMANDS.md](./RUN_COMMANDS.md)** - Quick reference for run commands
- **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** - How to test all features

### Project Management
- **[PROJECT_PLAN.md](./PROJECT_PLAN.md)** - 16-week development plan
- **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - Current progress and completion status
- **[CHECKLIST.md](./CHECKLIST.md)** - Detailed task checklist

### Technical Docs
- **[ML_MODELS_COMPREHENSIVE_REPORT.md](./ML_MODELS_COMPREHENSIVE_REPORT.md)** - All trained models, accuracy, how they work
- **[JWT_AUTHENTICATION.md](./JWT_AUTHENTICATION.md)** - How JWT authentication works
- **[ML_MODELS_RECOMMENDATION.md](./ML_MODELS_RECOMMENDATION.md)** - Why we chose these ML models
- **[CODE_COMMENTING_GUIDE.md](./CODE_COMMENTING_GUIDE.md)** - Code standards
- **[MODELS_EXPLAINED.md](./MODELS_EXPLAINED.md)** - Database models vs ML models explained

### Component READMEs
- **[backend/README.md](./backend/README.md)** - Backend API documentation
- **[frontend/README.md](./frontend/README.md)** - Frontend documentation
- **[ml_models/README.md](./ml_models/README.md)** - ML model training guide

## 🎭 User Roles

### Patient
- ✅ View own medical records
- ✅ Book appointments with doctors
- ✅ View prescriptions and diagnoses
- ❌ Cannot see other patients

### Doctor
- ✅ View all patients
- ✅ Create diagnoses using ML predictions
- ✅ Prescribe medicines
- ✅ Manage appointments

## 🔐 Authentication

- **JWT-based** authentication (no Firebase)
- Users register with **real email** + password
- Passwords are hashed (never stored as plain text)
- Access tokens expire in 1 hour, refresh tokens in 30 days

## 💾 Database Tables

- **users** - Login credentials (email, password_hash, role)
- **patients** - Patient profiles (linked to users)
- **doctors** - Doctor profiles (linked to users)
- **diagnoses** - Medical diagnoses (with ML predictions)
- **prescriptions** - Medicine prescriptions
- **appointments** - Appointment scheduling
- **drugs** - Drug catalog (16,780 drugs from DrugBank)

## 🤖 Machine Learning

### Best Models

1. **LightGBM** - 46.31% accuracy (exact disease match)
2. **Neural Network** - 59.41% F1-Micro (finds relevant diseases)

### How It Works

1. Doctor enters patient symptoms
2. Frontend sends symptoms to `/api/diagnosis/predict`
3. Backend loads ML model and vectorizer
4. Model predicts top 3 most likely diseases with confidence scores
5. Doctor reviews predictions and confirms diagnosis
6. Diagnosis saved to patient's medical record

## 🛠️ Tech Stack

### Frontend
- React 18 + Vite
- React Router DOM (routing)
- React Bootstrap (UI components)
- Axios (API calls)
- JWT authentication (localStorage)

### Backend
- Flask (Python web framework)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Flask-JWT-Extended (authentication)
- Flask-Migrate (database migrations)
- Flask-CORS (cross-origin requests)

### Machine Learning
- **scikit-learn** - Data preprocessing, ML utilities
- **LightGBM** - Best accuracy model
- **TensorFlow/Keras** - Neural network model
- **XGBoost** - Gradient boosting model
- **pandas** - Data manipulation
- **joblib** - Model persistence

## 📊 Project Structure

```
rehan/
├── backend/                 # Flask API
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   └── utils/          # Helper functions
│   ├── config.py           # Configuration
│   └── run.py              # Entry point
│
├── frontend/               # React app
│   ├── src/
│   │   ├── pages/          # Dashboard pages
│   │   ├── components/     # Reusable components
│   │   ├── context/        # Auth context
│   │   └── services/       # API service
│   └── package.json
│
├── ml_models/              # Machine Learning
│   ├── models/             # Trained models (.pkl files)
│   └── scripts/            # Training scripts
│
├── data/                   # Datasets
│   ├── drugbank_clean.csv  # 16,780 drugs
│   └── dataset_expanded_final.xlsx  # Training data
│
└── *.md                    # Documentation
```

## ✅ What's Complete

- ✅ Backend API (100%)
  - User authentication (JWT)
  - Patient/Doctor CRUD
  - Diagnosis prediction
  - Prescription management
  - Appointment scheduling
  
- ✅ Frontend (100%)
  - Login/Registration
  - Patient Dashboard
  - Doctor Dashboard
  - ML prediction interface
  
- ✅ ML Models (100%)
  - LightGBM trained
  - Neural Network trained
  - Integration with backend API
  
- ✅ Documentation (100%)
  - Setup guides
  - API documentation
  - Code comments

## 🎓 How to Use

### For Patients

1. Register with email + password (role: "patient")
2. Complete your profile
3. View your medical history
4. Book appointments with doctors
5. View prescriptions

### For Doctors

1. Register with email + password (role: "doctor")
2. Complete your profile
3. Go to "Diagnosis" tab
4. Select a patient
5. Enter symptoms (or choose from common symptoms)
6. Click "Predict" to get ML predictions
7. Review top 3 predicted diseases
8. Confirm diagnosis and add clinical notes
9. Save diagnosis

## 🌐 Deployment (Future)

The app is currently set up for local development. For production:
- Deploy backend to cloud (Heroku, AWS, Azure)
- Deploy frontend to Vercel/Netlify
- Use managed PostgreSQL (AWS RDS, Azure Database)
- Set up environment variables on cloud platform

## 📞 Support

- **Setup issues?** See [SETUP_AND_GUIDE.md](./SETUP_AND_GUIDE.md)
- **API questions?** See [backend/README.md](./backend/README.md)
- **ML questions?** See [ML_MODELS_COMPREHENSIVE_REPORT.md](./ML_MODELS_COMPREHENSIVE_REPORT.md)

---

**Built with ❤️ for better healthcare accessibility**
