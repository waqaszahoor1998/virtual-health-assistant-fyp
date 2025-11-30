# 🚀 Virtual Health Assistant - Complete Setup & User Guide

This is your ONE-STOP guide for everything: setup, how the code works, user roles, and database structure.

---

## 📋 Table of Contents

1. [Quick Start - Running the App](#quick-start---running-the-app)
2. [How Authentication Works (JWT & Email)](#how-authentication-works-jwt--email)
3. [Patient vs Doctor Roles](#patient-vs-doctor-roles)
4. [Database Structure](#database-structure)
5. [How the Code Works](#how-the-code-works)
6. [ML Models & Accuracy](#ml-models--accuracy)

---

## 🚀 Quick Start - Running the App

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **PostgreSQL 12+** (database)

### Step 1: Backend Setup

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows (Command Prompt):**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create `backend/.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/virtual_health_assistant
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

### Step 3: Database Setup

```bash
# Make sure PostgreSQL is running, then:
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 4: Train ML Models

```bash
cd ml_models/scripts
python feature_engineering.py
python train_lightgbm.py    # Best model: 46.31% accuracy
python train_neural_network.py    # Best F1-Micro: 59.41%
```

### Step 5: Run Backend

```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python run.py
```
Backend runs on `http://localhost:5000`

### Step 6: Run Frontend

Open a NEW terminal:
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

### ✅ Access the App

Open browser → `http://localhost:5173` → Register → Login

---

## 🔐 How Authentication Works (JWT & Email)

### Yes, JWT Works with Real Email!

**Registration:**
1. User provides **real email** + password + role (patient/doctor)
2. Backend validates email format (must have `@` and `.`)
3. Password is **hashed** using Werkzeug (never stored as plain text)
4. User record is saved in `users` table with email and hashed password

**Login:**
1. User enters **email** + password
2. Backend finds user by email in database
3. Password is checked against the stored hash
4. If valid, backend creates 2 JWT tokens:
   - **Access Token**: expires in 1 hour (for API requests)
   - **Refresh Token**: expires in 30 days (to get new access tokens)
5. Tokens are returned to frontend and stored in `localStorage`

**Making API Calls:**
- Frontend automatically adds `Authorization: Bearer <access_token>` to all API requests
- Backend validates token on every protected endpoint
- If token expires, frontend automatically uses refresh token to get a new one

**Important:** The email is just your login identifier - JWT doesn't send emails. It's like your username, but must be a valid email format.

---

## 👥 Patient vs Doctor Roles

### Patient Role - What They Can Do

**Dashboard Tabs:**
1. **Overview**
   - View their own profile info
   - See quick stats (upcoming appointments, active prescriptions)
   
2. **Prescriptions**
   - View ALL their prescriptions (past and current)
   - See drug names, dosage, instructions from doctors
   
3. **Appointments**
   - View their appointments (scheduled/completed/cancelled)
   - **Book new appointments** with any doctor
   - Cancel their appointments
   
4. **Medical History**
   - View their diagnosis history
   - See what diseases were diagnosed
   - Read clinical notes from doctors

**Permissions:**
- ✅ Can view ONLY their own data
- ✅ Can book appointments with any doctor
- ❌ Cannot see other patients
- ❌ Cannot create diagnoses
- ❌ Cannot prescribe medicines

**API Access:**
- `GET /api/patients` → Returns ONLY their own profile
- `GET /api/appointments` → Returns ONLY their appointments
- `GET /api/prescriptions/patient/:id` → ONLY if it's their own ID
- `POST /api/appointments` → Can book appointments

---

### Doctor Role - What They Can Do

**Dashboard Tabs:**
1. **Diagnosis** (Main Feature)
   - Select any patient from the database
   - Choose symptoms (from common list or add custom)
   - **Click "Predict"** → ML model predicts diseases
   - Review predictions (disease name + confidence %)
   - Confirm diagnosis and add clinical notes
   - Save diagnosis to patient's record
   
2. **Patients**
   - View ALL patients in the system
   - Search patients by name/phone
   - Select patient for diagnosis
   
3. **Appointments**
   - View ALL appointments (all patients)
   - See appointment details, status, dates

**Permissions:**
- ✅ Can view ALL patients
- ✅ Can create diagnoses for any patient
- ✅ Can view ALL appointments
- ✅ Can use ML prediction model
- ❌ Cannot view other doctors' profiles (only their own)

**API Access:**
- `GET /api/patients` → Returns ALL patients (no restriction)
- `GET /api/patients/:id` → Can view any patient
- `POST /api/diagnosis/predict` → Use ML model
- `POST /api/diagnosis` → Create diagnosis for any patient
- `GET /api/appointments` → Returns ALL appointments

---

## 💾 Database Structure

### Where User Login Details Are Stored

**`users` Table** (Main Authentication)
```sql
id              (auto-increment primary key)
email           (unique, used for login)
password_hash   (hashed password - NEVER plain text)
role            ('patient' or 'doctor')
created_at      (when account was created)
updated_at      (last modified)
is_active       (account enabled/disabled)
```

**How Login Works:**
1. User enters email: `john@example.com` + password: `mypass123`
2. Backend finds record in `users` table where email = `john@example.com`
3. Checks if `password_hash` matches the provided password (using bcrypt)
4. If match → generates JWT token with `user.id` inside
5. Returns token to frontend

---

### Where Patient Personal Info Is Stored

**`patients` Table** (Links to `users` via `user_id`)
```sql
id                (patient ID)
user_id           (foreign key to users.id - links to login account)
first_name        (e.g., "John")
last_name         (e.g., "Doe")
date_of_birth     (DOB for age calculation)
gender            (optional)
phone             (contact number)
address           (full address)
blood_type        (e.g., "O+")
allergies         (e.g., "Peanuts, Penicillin")
medical_history   (past conditions, surgeries - JSON format)
created_at        (timestamp)
updated_at        (timestamp)
```

**Relationship:**
- Each `User` (with role='patient') has ONE `Patient` profile
- `patient.user_id` → `user.id` (one-to-one)
- When patient logs in, system finds their `User` record, then loads their `Patient` profile

---

### Where Doctor Personal Info Is Stored

**`doctors` Table** (Links to `users` via `user_id`)
```sql
id                (doctor ID)
user_id           (foreign key to users.id - links to login account)
first_name        (e.g., "Dr. Sarah")
last_name         (e.g., "Smith")
specialization    (e.g., "Cardiology")
license_number    (unique medical license)
phone             (contact number)
hospital_clinic   (where they practice)
address           (practice address)
created_at        (timestamp)
updated_at        (timestamp)
```

**Relationship:**
- Each `User` (with role='doctor') has ONE `Doctor` profile
- `doctor.user_id` → `user.id` (one-to-one)

---

### Other Important Tables

**`diagnoses` Table** (Medical Records)
```sql
id              (diagnosis ID)
patient_id      (foreign key to patients.id)
doctor_id       (foreign key to doctors.id)
predicted_diseases   (ML model predictions - JSON)
confirmed_disease    (doctor's final diagnosis)
symptoms        (list of symptoms - JSON)
notes           (doctor's clinical notes)
created_at      (when diagnosis was made)
```

**`prescriptions` Table** (Medicine Records)
```sql
id              (prescription ID)
diagnosis_id    (foreign key to diagnoses.id)
patient_id      (foreign key to patients.id)
doctor_id       (foreign key to doctors.id)
drug_name       (medicine name)
dosage          (e.g., "500mg")
frequency       (e.g., "Twice daily")
duration        (e.g., "7 days")
instructions    (special instructions)
created_at      (timestamp)
```

**`appointments` Table** (Booking System)
```sql
id                  (appointment ID)
patient_id          (foreign key to patients.id)
doctor_id           (foreign key to doctors.id)
appointment_date    (date of appointment)
appointment_time    (time of appointment)
status              ('scheduled', 'completed', 'cancelled')
reason              (reason for visit)
notes               (additional notes)
created_at          (timestamp)
```

---

## ⚙️ How the Code Works

### Backend Architecture (Flask)

**Entry Point:** `backend/run.py`
- Starts Flask development server on port 5000
- Loads configuration from `backend/config.py`
- Initializes the app from `backend/app/__init__.py`

**App Factory:** `backend/app/__init__.py`
- Creates Flask app instance
- Connects to PostgreSQL database using SQLAlchemy
- Sets up JWT authentication (Flask-JWT-Extended)
- Enables CORS for frontend requests
- Registers API blueprints (routes)

**API Endpoints:** `backend/app/api/`
- `auth.py` - Registration, login, logout, token refresh
- `patients.py` - CRUD for patient profiles
- `doctors.py` - CRUD for doctor profiles
- `diagnosis.py` - ML prediction & diagnosis creation
- `drugs.py` - Drug search from DrugBank dataset
- `prescriptions.py` - Prescription management
- `appointments.py` - Appointment scheduling

**Database Models:** `backend/app/models/`
- Each file defines a database table (User, Patient, Doctor, etc.)
- Uses SQLAlchemy ORM (no need to write SQL)
- Relationships defined between tables (foreign keys)

**Example: How Login Works (Code Flow)**

1. **Frontend:** User fills login form → `LoginPage.jsx`
   ```javascript
   const handleLogin = async (e) => {
     await signIn(email, password)  // Calls AuthContext
   }
   ```

2. **AuthContext:** `frontend/src/context/AuthContext.jsx`
   ```javascript
   const signIn = async (email, password) => {
     const response = await authAPI.login({ email, password })
     localStorage.setItem('access_token', response.data.access_token)
     setUser(response.data.user)
   }
   ```

3. **API Service:** `frontend/src/services/api.js`
   ```javascript
   authAPI.login = (credentials) => {
     return api.post('/auth/login', credentials)
   }
   ```

4. **Backend API:** `backend/app/api/auth.py`
   ```python
   @api_bp.route('/auth/login', methods=['POST'])
   def login():
       email = data['email']
       user = User.query.filter_by(email=email).first()
       if user and user.check_password(password):
           access_token = create_access_token(identity=str(user.id))
           return jsonify({'access_token': access_token, 'user': user.to_dict()})
   ```

5. **User Model:** `backend/app/models/user.py`
   ```python
   def check_password(self, password):
       return check_password_hash(self.password_hash, password)
   ```

---

### Frontend Architecture (React + Vite)

**Entry Point:** `frontend/src/main.jsx`
- Mounts React app to DOM
- Wraps app with `BrowserRouter` (for routing)
- Wraps app with `AuthProvider` (for global auth state)

**Routing:** `frontend/src/App.jsx`
- Defines all routes:
  - `/` → Home/Login page
  - `/doctor/dashboard` → Doctor dashboard (protected)
  - `/patient/dashboard` → Patient dashboard (protected)

**Authentication:** `frontend/src/context/AuthContext.jsx`
- Provides `user`, `signIn`, `signUp`, `signOut` to all components
- Stores tokens in `localStorage`
- Checks if user is logged in on app load

**API Calls:** `frontend/src/services/api.js`
- Axios instance configured with base URL (`http://localhost:5000`)
- **Interceptor** automatically adds JWT token to every request:
  ```javascript
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })
  ```
- **Interceptor** handles token refresh if 401 error:
  ```javascript
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await api.post('/auth/refresh', {}, {
          headers: { Authorization: `Bearer ${refreshToken}` }
        })
        // Retry original request with new token
      }
    }
  )
  ```

---

### ML Model Integration

**Training:** `ml_models/scripts/`
- `feature_engineering.py` - Cleans data, creates TF-IDF vectors
- `train_lightgbm.py` - Trains LightGBM model (best accuracy: 46.31%)
- `train_neural_network.py` - Trains Neural Network (best F1: 59.41%)

**Saved Models:** `ml_models/models/`
- `symptom_vectorizer.pkl` - Converts symptoms to numbers
- `disease_encoder.pkl` - Converts diseases to numbers
- `lightgbm_model.pkl` - Trained model (193 MB)

**Backend ML Service:** `backend/app/utils/ml_service.py`
```python
def predict_diseases(symptoms):
    # Load models
    vectorizer = joblib.load('symptom_vectorizer.pkl')
    encoder = joblib.load('disease_encoder.pkl')
    model = joblib.load('lightgbm_model.pkl')
    
    # Convert symptoms to feature vector
    X = vectorizer.transform([symptoms])
    
    # Predict
    predictions = model.predict_proba(X)
    
    # Get top 3 diseases
    top_indices = predictions.argsort()[-3:]
    diseases = encoder.inverse_transform(top_indices)
    
    return diseases
```

**API Endpoint:** `backend/app/api/diagnosis.py`
```python
@api_bp.route('/diagnosis/predict', methods=['POST'])
@jwt_required()
def predict_diagnosis():
    symptoms = data['symptoms']  # e.g., ["fever", "headache"]
    predictions = predict_diseases(symptoms)
    return jsonify({'predictions': predictions})
```

**Frontend Usage:** `frontend/src/pages/DoctorDashboard.jsx`
```javascript
const handlePredict = async () => {
  const response = await diagnosisAPI.predict({
    symptoms: selectedSymptoms
  })
  setPredictions(response.data.predictions)
}
```

---

## 📊 ML Models & Accuracy

### Current Best Models

1. **LightGBM** - 46.31% accuracy
   - Best for exact disease match
   - Fast prediction (~50ms)
   - File: `lightgbm_model.pkl` (193 MB)

2. **Neural Network** - 59.41% F1-Micro score
   - Best for finding relevant diseases
   - Trained on 2,272 samples
   - File: `neural_network_model.h5` (32 MB)

### Dataset

- **Training samples:** 2,272 records
- **Diseases:** 1,140 unique diseases
- **Symptoms:** 5,000 unique symptoms (TF-IDF features)
- **Source:** Original dataset + Kaggle datasets (merged and cleaned)

### Why Accuracy is 46%?

- **Multi-label problem:** Each symptom set can map to multiple diseases
- **Sparse data:** Many diseases have only 1-2 training examples
- **Medical complexity:** Same symptoms can indicate different diseases

**For medical use:** 46% is actually decent for initial screening. The model suggests top 3 diseases, and the doctor makes the final diagnosis.

---

## 🎯 Summary

### Core Concepts

1. **JWT with Email:**
   - Email is your login username (must be valid format)
   - Password is hashed and stored securely
   - JWT tokens (access + refresh) manage sessions

2. **Two Roles:**
   - **Patients:** View own data, book appointments
   - **Doctors:** View all patients, create diagnoses, use ML predictions

3. **Database:**
   - `users` → login credentials
   - `patients`/`doctors` → personal info (linked to users)
   - `diagnoses`/`prescriptions`/`appointments` → medical records

4. **How It Works:**
   - Frontend (React) → API calls → Backend (Flask) → Database (PostgreSQL)
   - ML models trained separately, loaded by backend, used via API
   - JWT tokens secure all API requests

---

## 📞 Need Help?

- **Backend API docs:** `backend/README.md`
- **Frontend docs:** `frontend/README.md`
- **ML models report:** `ML_MODELS_COMPREHENSIVE_REPORT.md`
- **Testing guide:** `TESTING_GUIDE.md`

**Run Commands:**
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python run.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

Access at: `http://localhost:5173`

