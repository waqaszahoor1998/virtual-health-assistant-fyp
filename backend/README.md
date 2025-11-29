# Virtual Health Assistant - Backend API

Flask-based REST API backend for the Virtual Health Assistant application.

## 📋 Overview

This backend provides RESTful APIs for:
- User authentication and authorization (Firebase integration)
- Patient and doctor management
- AI-powered disease diagnosis from symptoms
- Drug suggestions from DrugBank database
- Prescription management
- Appointment scheduling
- Medical records management

## 🛠️ Tech Stack

- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Firebase Admin SDK + JWT
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
- Firebase project (for authentication)

### 2. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Required settings:
# - DATABASE_URL (PostgreSQL connection string)
# - SECRET_KEY (for Flask sessions)
# - JWT_SECRET_KEY (for JWT tokens)
# - FIREBASE_CREDENTIALS (path to Firebase service account JSON)
```

### 4. Database Setup

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

### 5. Run Development Server

```bash
# Run the Flask development server
python run.py

# Or use Flask CLI
flask run

# Server will start on http://localhost:5000
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/verify` - Verify token
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
```bash
export FLASK_ENV=production
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 📝 Database Models

### User
- Stores authentication information (Firebase UID, email, role)
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

## 🔐 Authentication Flow

1. Frontend authenticates user with Firebase
2. Frontend sends Firebase ID token to backend
3. Backend verifies token with Firebase Admin SDK
4. Backend creates/retrieves User record
5. Backend returns JWT token for subsequent requests
6. Frontend includes JWT token in Authorization header

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
- `firebase-admin` - Firebase Admin SDK
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

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL in .env file
# Format: postgresql://username:password@host:port/database
```

### Firebase Authentication Issues
- Ensure `FIREBASE_CREDENTIALS` path is correct in `.env`
- Verify Firebase service account JSON file exists
- Check Firebase project permissions

### Import Errors
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check Python path includes backend directory

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## 🔄 Development Workflow

1. Create feature branch
2. Make changes
3. Test locally
4. Commit changes
5. Push to repository
6. Create pull request

## 📞 Support

For issues or questions, refer to the main project README or contact the development team.

