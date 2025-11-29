# Models Explained - Virtual Health Assistant

## Overview

This project uses **TWO types of models**:

1. **Database Models** (SQLAlchemy) - For storing data in PostgreSQL
2. **Machine Learning Models** (XGBoost) - For disease prediction from symptoms

Let me explain both in detail:

---

## 1. Database Models (Data Storage)

### What Are They?

**Database models** are Python classes that represent database tables. They define:
- What data fields exist (columns)
- What type of data each field stores
- How different tables relate to each other

Think of them as **blueprints** for your database structure.

### Where Are They?

Located in: `backend/app/models/`

### Our 9 Database Models:

#### 1. **User Model** (`user.py`)
**Purpose**: Stores user authentication information

**What it stores**:
- Email address (for login)
- Password hash (encrypted password)
- User role (patient or doctor)
- Account status (active/inactive)
- Timestamps

**Used for**: User login, authentication, authorization

**Example**:
```python
User(
    email="doctor@example.com",
    password_hash="hashed_password",
    role="doctor"
)
```

---

#### 2. **Patient Model** (`patient.py`)
**Purpose**: Stores patient profile information

**What it stores**:
- Personal info: Name, DOB, gender, phone, address
- Medical info: Blood type, allergies, medical history

**Used for**: 
- Displaying patient profiles
- Storing patient medical records
- Linking to diagnoses, prescriptions, appointments

**Example**:
```python
Patient(
    user_id=1,
    first_name="John",
    last_name="Doe",
    blood_type="O+",
    allergies='["Peanuts", "Penicillin"]'
)
```

---

#### 3. **Doctor Model** (`doctor.py`)
**Purpose**: Stores doctor profile information

**What it stores**:
- Personal info: Name, specialization
- Professional info: License number, hospital/clinic, contact

**Used for**:
- Displaying doctor profiles
- Linking to diagnoses and appointments
- Doctor search functionality

**Example**:
```python
Doctor(
    user_id=2,
    first_name="Jane",
    last_name="Smith",
    specialization="Cardiology",
    license_number="MD12345"
)
```

---

#### 4. **Diagnosis Model** (`diagnosis.py`)
**Purpose**: Stores diagnosis records

**What it stores**:
- Patient ID (who the diagnosis is for)
- Doctor ID (who made the diagnosis)
- Symptoms (list of symptoms reported)
- Predicted diseases (ML model predictions)
- Confirmed disease (doctor's final diagnosis)
- Clinical notes

**Used for**:
- Recording diagnoses
- Storing ML predictions
- Medical history tracking

**Example**:
```python
Diagnosis(
    patient_id=1,
    doctor_id=1,
    symptoms='["fever", "headache"]',
    predicted_diseases='[{"disease": "Migraine", "confidence": 0.85}]',
    confirmed_disease="Migraine",
    notes="Patient responds well to rest"
)
```

---

#### 5. **Prescription Model** (`prescription.py`)
**Purpose**: Stores prescription records

**What it stores**:
- Diagnosis ID (which diagnosis led to this prescription)
- Patient ID
- Doctor ID
- Drug information (name, DrugBank ID)
- Dosage, frequency, duration
- Instructions

**Used for**:
- Prescribing medications
- Tracking prescription history
- Patient medication management

**Example**:
```python
Prescription(
    diagnosis_id=1,
    patient_id=1,
    doctor_id=1,
    drugbank_id="DB00001",
    drug_name="Aspirin",
    dosage="500mg",
    frequency="Twice daily",
    duration="7 days"
)
```

---

#### 6. **Appointment Model** (`appointment.py`)
**Purpose**: Stores appointment scheduling information

**What it stores**:
- Patient ID
- Doctor ID
- Appointment date and time
- Status (scheduled/completed/cancelled)
- Reason for appointment
- Notes

**Used for**:
- Booking appointments
- Appointment management
- Calendar scheduling

**Example**:
```python
Appointment(
    patient_id=1,
    doctor_id=1,
    appointment_date=datetime(2024, 3, 15, 14, 30),
    status="scheduled",
    reason="Follow-up appointment"
)
```

---

#### 7. **Drug Model** (`drug.py`)
**Purpose**: Drug catalog/reference table

**What it stores**:
- DrugBank ID (unique identifier)
- Drug name
- Description
- Indications (what it's used for)
- Mechanism of action (how it works)

**Used for**:
- Drug search functionality
- Prescription suggestions
- Drug information lookup

**Example**:
```python
Drug(
    drugbank_id="DB00001",
    name="Aspirin",
    indication="Pain relief, fever reduction"
)
```

---

#### 8. **Disease Model** (`disease.py`)
**Purpose**: Disease catalog/reference table

**What it stores**:
- Disease name
- Description
- Category/type

**Used for**:
- Disease reference
- Disease search
- Categorizing diagnoses

**Example**:
```python
Disease(
    name="Migraine",
    description="Neurological condition",
    category="Neurological"
)
```

---

#### 9. **Symptom Model** (`symptom.py`)
**Purpose**: Symptom catalog/reference table

**What it stores**:
- Symptom name
- Description
- Category/type

**Used for**:
- Symptom reference
- Symptom selection in UI
- Symptom categorization

**Example**:
```python
Symptom(
    name="Fever",
    description="Elevated body temperature",
    category="General"
)
```

---

### How Database Models Are Used

#### 1. **Creating Records** (Saving Data):
```python
# Create a new patient
patient = Patient(
    user_id=1,
    first_name="John",
    last_name="Doe"
)
db.session.add(patient)
db.session.commit()
```

#### 2. **Reading Records** (Retrieving Data):
```python
# Get all patients
patients = Patient.query.all()

# Get patient by ID
patient = Patient.query.get(1)

# Search patients
patients = Patient.query.filter_by(blood_type="O+").all()
```

#### 3. **Updating Records**:
```python
patient = Patient.query.get(1)
patient.phone = "+1234567890"
db.session.commit()
```

#### 4. **Deleting Records**:
```python
patient = Patient.query.get(1)
db.session.delete(patient)
db.session.commit()
```

---

## 2. Machine Learning Models (AI Prediction)

### What Are They?

**Machine Learning models** are trained algorithms that can make predictions based on patterns learned from data.

In this project, we use ML models to **predict diseases from symptoms**.

### Where Are They?

Located in: `ml_models/models/`

### Our ML Model:

#### **XGBoost Model** (`xgboost_model.pkl`)
**Purpose**: Predict diseases from symptoms

**What it does**:
1. Takes a list of symptoms as input
2. Analyzes the symptoms
3. Predicts possible diseases with confidence scores

**How it works**:
- **Input**: List of symptoms (e.g., ["fever", "headache", "nausea"])
- **Processing**: 
  - Converts symptoms to numbers (TF-IDF vectorization)
  - Uses trained model to predict diseases
  - Calculates confidence scores (0-100%)
- **Output**: List of predicted diseases with confidence scores

**Example**:
```python
# Input symptoms
symptoms = ["fever", "headache", "muscle pain"]

# ML model predicts
predictions = [
    {"disease": "Influenza", "confidence": 0.92},
    {"disease": "Common Cold", "confidence": 0.65},
    {"disease": "Migraine", "confidence": 0.45}
]
```

**Used for**:
- Disease prediction in diagnosis flow
- Assisting doctors in diagnosis
- Quick symptom analysis

---

### How ML Models Are Used

#### 1. **Loading the Model**:
```python
from app.utils.ml_service import get_ml_service

ml_service = get_ml_service()
ml_service.load_models()
```

#### 2. **Making Predictions**:
```python
symptoms = ["fever", "headache"]
predictions = ml_service.predict_diseases(
    symptoms=symptoms,
    model_type="xgboost",
    top_k=5
)
```

#### 3. **In the API**:
```python
# POST /api/diagnosis/predict
{
    "symptoms": ["fever", "headache"],
    "top_k": 5
}

# Response
{
    "predictions": [
        {"disease": "Influenza", "confidence": 0.92},
        {"disease": "Common Cold", "confidence": 0.65}
    ]
}
```

#### 4. **In the Frontend**:
```javascript
// Doctor selects symptoms and clicks "Predict"
const response = await diagnosisAPI.predict(["fever", "headache"]);
// Displays predictions with confidence scores
```

---

## Key Differences

| Aspect | Database Models | ML Models |
|--------|----------------|-----------|
| **Purpose** | Store data | Make predictions |
| **Type** | Python classes (SQLAlchemy) | Trained algorithms (XGBoost) |
| **Input** | Data fields | Symptoms (list) |
| **Output** | Database records | Disease predictions |
| **Used for** | CRUD operations | AI-powered predictions |
| **Location** | `backend/app/models/` | `ml_models/models/` |
| **File format** | `.py` (Python code) | `.pkl` (Pickle file) |

---

## Real-World Example: Complete Flow

### Scenario: Doctor diagnoses a patient

#### Step 1: Get Patient (Database Model)
```python
patient = Patient.query.get(patient_id)  # Database model
```

#### Step 2: Select Symptoms
```python
symptoms = ["fever", "headache", "nausea"]
```

#### Step 3: Predict Diseases (ML Model)
```python
predictions = ml_service.predict_diseases(symptoms)  # ML model
# Returns: [{"disease": "Migraine", "confidence": 0.85}]
```

#### Step 4: Save Diagnosis (Database Model)
```python
diagnosis = Diagnosis(
    patient_id=patient.id,  # Database model
    doctor_id=doctor.id,    # Database model
    symptoms=json.dumps(symptoms),
    predicted_diseases=json.dumps(predictions),  # From ML model
    confirmed_disease="Migraine"
)
db.session.add(diagnosis)  # Database model
db.session.commit()
```

---

## Summary

### Database Models = **Storing & Retrieving Data**
- Like a filing cabinet - stores all your information
- Examples: Patient records, appointments, prescriptions
- You create, read, update, delete data

### ML Models = **Making Intelligent Predictions**
- Like a smart assistant - analyzes and predicts
- Example: Predict diseases from symptoms
- You give it input, it gives you predictions

### They Work Together:
1. **Database models** store patient data, symptoms, diagnoses
2. **ML models** analyze symptoms and predict diseases
3. **Database models** save the predictions and doctor's final diagnosis

---

## Files Reference

### Database Models:
- `backend/app/models/user.py` - User authentication
- `backend/app/models/patient.py` - Patient profiles
- `backend/app/models/doctor.py` - Doctor profiles
- `backend/app/models/diagnosis.py` - Diagnosis records
- `backend/app/models/prescription.py` - Prescriptions
- `backend/app/models/appointment.py` - Appointments
- `backend/app/models/drug.py` - Drug catalog
- `backend/app/models/disease.py` - Disease catalog
- `backend/app/models/symptom.py` - Symptom catalog

### ML Models:
- `ml_models/models/xgboost_model.pkl` - Trained XGBoost model
- `ml_models/models/symptom_vectorizer.pkl` - Feature processor
- `ml_models/models/disease_encoder.pkl` - Disease encoder
- `backend/app/utils/ml_service.py` - ML service wrapper

---

**Both types of models are essential for the Virtual Health Assistant to function!**

