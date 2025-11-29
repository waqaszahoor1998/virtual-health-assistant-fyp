# Virtual Health Assistant - Backend API

Flask-based REST API backend for the Virtual Health Assistant application.

## 📋 Overview

This backend provides RESTful APIs for:
- User authentication and authorization (JWT-based)
- Patient and doctor management
- AI-powered disease diagnosis from symptoms
- Drug suggestions from DrugBank database
- Prescription management
- Appointment scheduling
- Medical records management

## 🛠️ Tech Stack

- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **Password Hashing**: Werkzeug
- **ML Integration**: XGBoost, Random Forest, scikit-learn
- **API Documentation**: Flask-Swagger-UI

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── diagnosis.py
│   │   ├── prescription.py
│   │   ├── appointment.py
│   │   ├── drug.py
│   │   ├── disease.py
│   │   └── symptom.py
│   ├── api/                 # API endpoints (blueprints)
│   │   ├── auth.py
│   │   ├── patients.py
│   │   ├── doctors.py
│   │   ├── diagnosis.py
│   │   ├── drugs.py
│   │   ├── prescriptions.py
│   │   └── appointments.py
│   └── utils/               # Utility functions
├── config.py                # Configuration settings
├── run.py                   # Development server entry point
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher

### 2. Install Dependencies

#### macOS/Linux:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Windows (Command Prompt):

```cmd
REM Navigate to backend directory
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt
```

#### Windows (PowerShell):

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

#### macOS/Linux:

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Required settings:
# - DATABASE_URL (PostgreSQL connection string)
# - SECRET_KEY (for Flask sessions)
# - JWT_SECRET_KEY (for JWT tokens)
```

#### Windows (Command Prompt):

```cmd
REM Copy environment template
copy .env.example .env

REM Edit .env file with your configuration
REM Required settings:
REM - DATABASE_URL (PostgreSQL connection string)
REM - SECRET_KEY (for Flask sessions)
REM - JWT_SECRET_KEY (for JWT tokens)
```

#### Windows (PowerShell):

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env file with your configuration
# Required settings:
# - DATABASE_URL (PostgreSQL connection string)
# - SECRET_KEY (for Flask sessions)
# - JWT_SECRET_KEY (for JWT tokens)
```

**Required Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask session secret key
- `JWT_SECRET_KEY` - JWT token signing key
- `CORS_ORIGINS` - Allowed frontend origins (default: http://localhost:3000)

### 4. Database Setup

#### macOS/Linux:

```bash
# Make sure PostgreSQL is running and create database
createdb virtual_health_assistant

# Initialize database migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

#### Windows:

```cmd
REM Open Command Prompt and create database
psql -U postgres
CREATE DATABASE virtual_health_assistant;
\q

REM Or using command line:
psql -U postgres -c "CREATE DATABASE virtual_health_assistant;"

REM Initialize database migrations (from backend directory)
cd backend
venv\Scripts\activate.bat
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Windows PostgreSQL Connection:**
- Default username: `postgres`
- Default port: `5432`
- Format: `postgresql://postgres:your_password@localhost:5432/virtual_health_assistant`

### 5. Run Development Server

#### macOS/Linux:

```bash
# Run the Flask development server
python run.py

# Or use Flask CLI
flask run

# Server will start on http://localhost:5000
```

#### Windows:

```cmd
REM Run the Flask development server
python run.py

REM Or use Flask CLI
flask run

REM Server will start on http://localhost:5000
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout
- `GET /api/auth/verify` - Verify token
- `GET /api/auth/user` - Get current user

### Patients
- `GET /api/patients` - List patients
- `GET /api/patients/:id` - Get patient details
- `POST /api/patients` - Create patient
- `PUT /api/patients/:id` - Update patient
- `DELETE /api/patients/:id` - Delete patient

### Doctors
- `GET /api/doctors` - List doctors
- `GET /api/doctors/:id` - Get doctor details

### Diagnosis
- `POST /api/diagnosis/predict` - Predict diseases from symptoms (ML model)

### Drugs
- `GET /api/drugs/search` - Search drugs from DrugBank
- `POST /api/drugs/suggest` - Suggest drugs for diagnosis

### Prescriptions
- `POST /api/prescriptions` - Create prescription
- `GET /api/prescriptions/:id` - Get prescription

### Appointments
- `POST /api/appointments` - Create appointment
- `GET /api/appointments` - List appointments

## 🔧 Configuration

Configuration is managed through environment variables and the `config.py` file:

- **Development**: Uses `DevelopmentConfig` (debug mode enabled)
- **Production**: Uses `ProductionConfig` (security optimized)
- **Testing**: Uses `TestingConfig` (in-memory database)

Set `FLASK_ENV` environment variable to switch configurations:

#### macOS/Linux:
```bash
export FLASK_ENV=production
```

#### Windows (Command Prompt):
```cmd
set FLASK_ENV=production
```

#### Windows (PowerShell):
```powershell
$env:FLASK_ENV="production"
```

## 🧪 Testing

#### macOS/Linux/Windows:
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 📝 Database Models

### User
- Stores authentication information (email, password hash, role)
- Password hashing using Werkzeug
- Links to Patient or Doctor profiles

### Patient
- Patient personal and medical information
- Linked to User via one-to-one relationship

### Doctor
- Doctor professional information
- Linked to User via one-to-one relationship

### Diagnosis
- Stores diagnosis records (symptoms, predicted diseases, confirmed diagnosis)
- Links Patient and Doctor

### Prescription
- Stores prescription details (drugs, dosage, instructions)
- Links to Diagnosis

### Appointment
- Stores appointment scheduling information
- Links Patient and Doctor

### Drug
- Drug information from DrugBank database

### Disease
- Disease information and classification

### Symptom
- Symptom catalog for ML training

## 🔐 Authentication Flow (JWT-based)

1. User registers/logs in with email and password
2. Backend validates credentials and hashes password
3. Backend creates JWT access token and refresh token
4. Tokens are returned to frontend
5. Frontend stores tokens and includes access token in Authorization header
6. Backend verifies JWT token on each request
7. When access token expires, frontend uses refresh token to get new access token

## 🤖 ML Model Integration

ML models are stored in `../ml_models/models/` directory.

Prediction endpoint (`/api/diagnosis/predict`):
1. Receives symptoms from request
2. Loads trained XGBoost/Random Forest model
3. Preprocesses symptoms into feature vector
4. Returns predicted diseases with confidence scores

## 📦 Dependencies

Key dependencies:
- `flask` - Web framework
- `flask-sqlalchemy` - ORM for database
- `flask-jwt-extended` - JWT authentication
- `werkzeug` - Password hashing utilities
- `psycopg2-binary` - PostgreSQL driver
- `pandas` - Data processing
- `scikit-learn` - Machine learning
- `xgboost` - Gradient boosting model

See `requirements.txt` for complete list.

## 🚨 Important Notes

- **Never commit `.env` file** - Contains sensitive credentials
- **Use environment variables** for all sensitive configuration
- **Enable HTTPS** in production
- **Implement rate limiting** for API endpoints
- **Validate all inputs** to prevent SQL injection and XSS
- **Use strong JWT secret keys** in production

## 🐛 Troubleshooting

### Database Connection Issues

#### macOS/Linux:
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL in .env file
# Format: postgresql://username:password@host:port/database
```

#### Windows:
```cmd
REM Check PostgreSQL is running
psql --version

REM Test connection
psql -U postgres -c "SELECT version();"

REM Verify DATABASE_URL in .env file
REM Format: postgresql://username:password@host:port/database
```

**Common Windows Issues:**
- PostgreSQL service not running: Start from Services (`services.msc`)
- Port 5432 blocked: Check Windows Firewall
- Connection refused: Verify PostgreSQL is running on port 5432

### Import Errors

#### macOS/Linux/Windows:
```bash
# Ensure virtual environment is activated
# macOS/Linux:
source venv/bin/activate

# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Check Python path includes backend directory
python -c "import sys; print(sys.path)"
```

### Port Already in Use

#### macOS/Linux:
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

#### Windows:
```cmd
REM Find process using port 5000
netstat -ano | findstr :5000

REM Kill process (replace PID)
taskkill /PID <PID> /F
```

### PowerShell Execution Policy (Windows)

If you see "execution of scripts is disabled on this system":

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [JWT Authentication Guide](../JWT_AUTHENTICATION.md)

## 🔄 Development Workflow

1. Create feature branch
2. Make changes
3. Test locally
4. Commit changes
5. Push to repository
6. Create pull request

## 📞 Support

For issues or questions, refer to:
- Main project README: `../README.md`
- JWT Authentication guide: `../JWT_AUTHENTICATION.md`
- Quick Start guide: `../QUICK_START.md`
