# Quick Start Guide - Virtual Health Assistant

## 🚀 Getting Started in 5 Steps

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and Firebase credentials

# Initialize database (if PostgreSQL is running)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run backend server
python run.py
# Backend will run on http://localhost:5000
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your Firebase configuration

# Run frontend development server
npm run dev
# Frontend will run on http://localhost:3000
```

### Step 3: Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project (or use existing)
3. Enable Authentication > Email/Password
4. Go to Project Settings > Your apps
5. Copy Firebase configuration values
6. Paste into `frontend/.env` file

### Step 4: Database Setup

1. Install PostgreSQL (if not installed)
2. Create database:
   ```bash
   createdb virtual_health_assistant
   ```
3. Update `backend/.env` with database URL:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/virtual_health_assistant
   ```

### Step 5: Test the Setup

1. Open browser to `http://localhost:3000`
2. Click "Sign Up" to create account
3. Login with your credentials
4. You should see the dashboard!

## 📁 Project Structure Overview

```
rehan/
├── backend/          # Flask API server
│   ├── app/         # Application code
│   ├── config.py    # Configuration
│   └── run.py       # Entry point
├── frontend/        # React application
│   ├── src/         # Source code
│   └── package.json # Dependencies
├── data/            # Data files
│   ├── raw/         # Original datasets
│   └── processed/   # Cleaned data
├── ml_models/       # ML model files
│   ├── scripts/     # Training scripts
│   └── models/      # Trained models
└── docs/            # Documentation
```

## 🔧 Environment Variables Needed

### Backend (.env)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
FIREBASE_CREDENTIALS=path/to/firebase-credentials.json
```

### Frontend (.env)
```
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=your-app-id
```

## ✅ Verification Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 3000
- [ ] PostgreSQL database created and accessible
- [ ] Firebase project created and authentication enabled
- [ ] Environment variables configured
- [ ] Can access http://localhost:3000
- [ ] Can create account and login

## 🐛 Common Issues

### Backend won't start
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env is correct
- Check all dependencies installed: `pip list`

### Frontend won't start
- Check Node.js version: `node --version` (should be 16+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Firebase env variables are set

### Database connection error
- Verify PostgreSQL is installed and running
- Check database exists: `psql -l`
- Verify username/password in DATABASE_URL

### Authentication not working
- Verify Firebase Authentication is enabled
- Check Firebase config values in frontend/.env
- Verify Firebase project ID matches

## 📚 Next Steps

1. **Data Preparation**: Run data cleaning scripts
   ```bash
   python ml_models/scripts/analyze_data.py
   ```

2. **ML Model Training**: Train models with cleaned data
   ```bash
   python ml_models/scripts/train_models.py
   ```

3. **API Development**: Implement remaining endpoints
   - See `backend/README.md` for API structure

4. **Frontend Development**: Build out dashboard pages
   - See `frontend/README.md` for component structure

## 📞 Need Help?

- Check detailed READMEs:
  - `backend/README.md` - Backend documentation
  - `frontend/README.md` - Frontend documentation
- Review project plan: `PROJECT_PLAN.md`
- Check ML recommendations: `ML_MODELS_RECOMMENDATION.md`
- Review dataset info: `DATASET_RECOMMENDATIONS.md`

