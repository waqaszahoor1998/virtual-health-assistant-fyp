# Virtual Health Assistant - Project Repository

## 📋 Overview

This is a **Final Year Project** for a Virtual Health Assistant - a web-based platform that helps both clinical doctors and patients with AI-powered disease diagnosis and verified medicine suggestions.

**Team Members:**
- Muhammad Rehan Ishaq (01-134212-124) - Frontend & UI
- Syed Farman Ali (01-134222-181) - Backend & AI

**Supervisor:** Dr. Adil Khan

---

## 📊 Data Summary

### Datasets Available:

| Dataset | Records | Purpose | Status |
|---------|---------|---------|--------|
| **drugbank_clean.csv** | 16,780 drugs | Medicine suggestion system | ✅ Ready |
| **dataset 2 final.xlsx** | 3,963 records | ML training data | ⚠️ Needs cleaning |
| **SMILIES.xlsx** | 738 drugs | Chemical structures (optional) | ✅ Ready |

### Key Statistics:
- **Symptoms available**: 1,848 records (46.6% of training data)
- **Diseases mapped**: 2,318 records (58.5% of training data)
- **Drug mappings**: 3,835 records (96.8% have drugbank-id)
- **Top diseases**: UTI (23), Asthma (18), Hypertension (14), COPD (12)
- **Data overlap**: 99.6% of training drugs exist in DrugBank ✅

---

## 🎯 Project Goals

1. ✅ AI-powered disease prediction from symptoms (ML models)
2. ✅ Verified medicine suggestions from DrugBank database
3. ✅ Doctor portal for patient management & prescriptions
4. ✅ Patient portal for medical records & appointments
5. ✅ Secure authentication & role-based access

---

## 🛠️ Tech Stack

### Frontend
- **React.js 18** - Modern UI library
- **Vite 5** - Fast build tool
- **React Router DOM 6** - Client-side routing
- **Bootstrap 5 + React Bootstrap** - UI framework
- **JWT Authentication** - Token-based auth (no Firebase needed)
- **Axios** - HTTP client with JWT token handling

### Backend
- **Flask 3.0** - Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **JWT (Flask-JWT-Extended)** - Token-based authentication
- **Werkzeug** - Password hashing utilities

### Machine Learning (Updated!)
- **XGBoost** ⭐ (Primary - Recommended, 75-85% accuracy)
- **Random Forest** (Baseline comparison)
- **Neural Networks** (Advanced, optional)
- **SVM** (For comparison)

*Note: Naive Bayes replaced with XGBoost for better accuracy*

### Deployment
- Cloud Server (TBD)

---

## 📁 Project Structure

```
rehan/
├── backend/                 # Flask API server
│   ├── app/                # Application code
│   │   ├── models/         # Database models
│   │   ├── api/            # API endpoints
│   │   └── utils/          # Utility functions
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   └── run.py              # Entry point
├── frontend/               # React application
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API & Firebase
│   │   └── context/        # React Context
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── data/                   # Data files
│   ├── raw/                # Original datasets
│   └── processed/          # Cleaned data
├── ml_models/              # ML model files
│   ├── scripts/            # Training scripts
│   └── models/             # Trained models
├── datasets/               # Additional datasets
├── docs/                   # Documentation
│   └── VirHeaAss..docx     # Project proposal
├── PROJECT_PLAN.md         # Detailed 16-week plan
├── EXECUTIVE_SUMMARY.md    # Quick overview
├── ML_MODELS_RECOMMENDATION.md  # ML model guide
├── DATASET_RECOMMENDATIONS.md   # Dataset expansion guide
├── QUICK_START.md          # Setup instructions
└── README.md               # This file
```

---

## 🚀 Quick Start

### Complete Setup Instructions

See **QUICK_START.md** for detailed setup guide.

**Quick Commands:**

```bash
# Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py  # Runs on http://localhost:5000

# Frontend Setup (in new terminal)
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

### Analyze the Data
```bash
cd ml_models/scripts
python analyze_data.py
```

### Review Documentation
- **QUICK_START.md** - Setup instructions
- **PROJECT_PLAN.md** - Detailed 16-week plan
- **ML_MODELS_RECOMMENDATION.md** - ML model guide
- **DATASET_RECOMMENDATIONS.md** - Dataset expansion
- **backend/README.md** - Backend API docs
- **frontend/README.md** - Frontend docs

---

## 📋 Project Phases

1. **Phase 1** (Weeks 1-2): Data Preparation & Analysis
2. **Phase 2** (Weeks 3-5): Machine Learning Model Development
3. **Phase 3** (Weeks 6-8): Backend Development
4. **Phase 4** (Weeks 9-11): Frontend Development
5. **Phase 5** (Weeks 12-14): Integration & Testing
6. **Phase 6** (Weeks 15-16): Deployment & Documentation

---

## 📈 Current Status

✅ **Completed:**
- ✅ Project proposal reviewed
- ✅ Data files analyzed and organized
- ✅ Complete project structure created
- ✅ Flask backend setup with models and API structure
- ✅ React frontend setup with routing and authentication
- ✅ ML model recommendations (XGBoost replacing Naive Bayes)
- ✅ Dataset expansion recommendations
- ✅ Comprehensive documentation

⏳ **In Progress:**
- 🔄 Backend API implementation (models ready, endpoints need implementation)
- 🔄 Frontend page components (structure ready, needs content)
- ⏳ Data preprocessing scripts

⏳ **Next Steps:**
- Data cleaning and preprocessing
- ML model training (XGBoost + Random Forest)
- Complete API endpoint implementations
- Build out frontend dashboard pages
- Integrate ML models with backend

---

## 🔍 Key Insights from Data Analysis

### Strengths:
- ✅ Large DrugBank database (16,780 drugs)
- ✅ Good symptom-disease mapping (1,848 symptom records)
- ✅ High overlap between datasets (99.6% of training drugs in DrugBank)
- ✅ Clear project objectives

### Areas for Improvement:
- ⚠️ Symptoms need text preprocessing (currently comma-separated strings)
- ⚠️ Some missing data (53.4% of records lack symptoms)
- ⚠️ Need to handle multi-label classification (multiple diseases per patient)
- ⚠️ Create disease → drug mapping from DrugBank indications

### Opportunities:
- 💡 Can expand symptom database
- 💡 Can add drug interaction checking
- 💡 Can enhance with SMILES chemical structures
- 💡 Can add more ML features

---

## 📚 Documentation

### Getting Started
- **QUICK_START.md**: Step-by-step setup guide
- **README.md**: This file - project overview

### Authentication
- **JWT_AUTHENTICATION.md**: Complete JWT authentication guide
- **AUTHENTICATION_CHANGES.md**: Summary of Firebase → JWT migration

### Planning & Strategy
- **PROJECT_PLAN.md**: Comprehensive 16-week development plan
- **EXECUTIVE_SUMMARY.md**: Quick overview and insights
- **ML_MODELS_RECOMMENDATION.md**: ML model selection guide
- **DATASET_RECOMMENDATIONS.md**: Dataset expansion strategy

### Development Docs
- **backend/README.md**: Backend API documentation
- **frontend/README.md**: Frontend documentation
- **CHECKLIST.md**: Development checklist

### Data & ML
- **ml_models/scripts/analyze_data.py**: Data analysis script

---

## ⚠️ Important Notes

1. **Medical Disclaimer**: This system is for educational purposes and should not replace professional medical advice.

2. **Data Privacy**: Patient data must be encrypted and securely stored per healthcare regulations.

3. **Model Accuracy**: ML models will be trained and evaluated, with limitations clearly documented.

---

## 📞 Contact & Support

For questions or issues, refer to the project proposal document or contact the supervisor:
- **Dr. Adil Khan**

---

## 📝 License

This is an academic project. All rights reserved.

---

**Last Updated**: Initial project setup and data analysis complete
**Status**: Ready to begin Phase 1 - Data Preparation

