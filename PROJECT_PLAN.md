# Virtual Health Assistant - Project Plan

## Project Overview
Based on the project proposal document and available datasets, this is a **Virtual Health Assistant** web application that helps both clinical doctors and patients with:
- AI-powered disease diagnosis from symptoms
- Verified medicine suggestions
- Patient portal for medical records, prescriptions, and appointments
- Doctor portal for patient management

---

## 📋 Data Analysis Summary

### Available Datasets:

1. **VirHeaAss..docx** (Project Proposal)
   - Defines project scope, objectives, and methodology
   - Tech stack: React.js, Flask/Django, PostgreSQL, Firebase
   - ML models: Naïve Bayes, Random Forest, SVM, XGBoost

2. **drugbank_clean.csv** (37,613 rows)
   - Comprehensive drug database from DrugBank
   - Columns: drugbank-id, name, description, indication, mechanism-of-action, etc.
   - Use: Medicine suggestion system

3. **dataset 2 final.xlsx** (3,963 rows)
   - **Symptoms**: 1,848 entries
   - **Diseases**: 2,318 entries
   - **Conditions**: 1,226 entries
   - **Therapies**: 340 entries
   - **Drug mappings**: 3,835+ drugbank-id and name entries
   - **Indications**: 3,612 entries
   - Use: Training data for disease prediction models

4. **SMILIES.xlsx** (738 rows)
   - Chemical structures in SMILES notation
   - Columns: drugbank-id, name, smilies
   - Use: Chemical structure visualization (optional feature)

---

## 🎯 Project Plan

### Phase 1: Data Preparation & Analysis (Week 1-2)

#### Tasks:
- [ ] **Data Cleaning & Preprocessing**
  - Clean and standardize symptoms in `dataset 2 final.xlsx`
  - Extract and normalize symptom lists (currently comma-separated)
  - Map symptoms to diseases with confidence scores
  - Clean drugbank data and create searchable index
  
- [ ] **Data Integration**
  - Create unified database schema
  - Link symptoms → diseases → drugs (using drugbank-id)
  - Create mappings: disease → recommended drugs from DrugBank
  
- [ ] **Data Validation**
  - Check data quality and completeness
  - Handle missing values
  - Validate drugbank-id references across datasets

#### Deliverables:
- Cleaned CSV/JSON datasets
- Database schema design
- Data mapping documentation

---

### Phase 2: Machine Learning Model Development (Week 3-5)

#### Tasks:
- [ ] **Feature Engineering**
  - Convert symptoms to feature vectors (TF-IDF, Bag of Words, or embeddings)
  - Create symptom → disease mapping matrix
  - Handle multi-label classification (one patient can have multiple diseases)
  
- [ ] **Model Training**
  - **Naïve Bayes**: Baseline model for symptom → disease prediction
  - **Random Forest**: Ensemble method for better accuracy
  - **SVM (Support Vector Machine)**: For non-linear relationships
  - **XGBoost**: Gradient boosting for optimal performance
  
- [ ] **Model Evaluation**
  - Split data: 70% train, 15% validation, 15% test
  - Metrics: Accuracy, Precision, Recall, F1-score, Confusion Matrix
  - Compare all 4 models and select best performer
  
- [ ] **Model Deployment Preparation**
  - Save trained models (pickle/joblib format)
  - Create prediction API endpoints

#### Deliverables:
- 4 trained ML models
- Model comparison report
- Model accuracy metrics
- Prediction API functions

---

### Phase 3: Backend Development (Week 6-8)

#### Tasks:
- [ ] **Technology Stack Setup**
  - Choose Flask or Django (based on team preference)
  - Set up PostgreSQL database
  - Configure Firebase for authentication
  
- [ ] **Database Schema Design**
  ```
  Tables needed:
  - Users (doctors, patients) - Firebase UID
  - Patients (patient info, linked to users)
  - Doctors (doctor info, linked to users)
  - Symptoms (symptom database)
  - Diseases (disease database)
  - Drugs (drugbank data)
  - Diagnoses (patient_id, symptoms, predicted_diseases, doctor_notes)
  - Prescriptions (diagnosis_id, drugbank-id, dosage, instructions)
  - Appointments (patient_id, doctor_id, date_time, status)
  - Medical_Records (patient_id, visit_date, notes, reports)
  ```

- [ ] **API Development**
  - `/api/auth/*` - Firebase authentication endpoints
  - `/api/patients/*` - Patient CRUD operations
  - `/api/doctors/*` - Doctor management
  - `/api/diagnosis/predict` - ML model prediction endpoint
  - `/api/drugs/search` - Drug search from DrugBank
  - `/api/drugs/suggest` - Drug suggestions based on diagnosis
  - `/api/prescriptions/*` - Prescription management
  - `/api/appointments/*` - Appointment booking system
  - `/api/records/*` - Medical records access

- [ ] **ML Model Integration**
  - Load trained models
  - Create prediction service
  - Add drug suggestion logic (diagnosis → drugs from DrugBank)

- [ ] **Security & Validation**
  - Input validation for symptoms
  - Role-based access control (doctor vs patient)
  - Data encryption for sensitive information
  - API rate limiting

#### Deliverables:
- Complete backend API
- PostgreSQL database with sample data
- Firebase authentication working
- ML prediction service integrated

---

### Phase 4: Frontend Development (Week 9-11)

#### Tasks:
- [ ] **Setup & Configuration**
  - Initialize React.js project
  - Install dependencies (React Router, Axios, Bootstrap, etc.)
  - Configure API endpoints
  
- [ ] **Doctor Portal**
  - Login/Registration page
  - Dashboard (patient list, appointments, recent diagnoses)
  - Patient search and profile view
  - Diagnosis page:
    - Symptom input interface
    - Real-time AI disease prediction display
    - Drug suggestion panel (from DrugBank)
    - Manual diagnosis override option
    - Prescription creation form
  - Patient history view
  - Appointment management

- [ ] **Patient Portal**
  - Login/Registration page
  - Dashboard (upcoming appointments, recent visits)
  - Medical history timeline
  - Prescription viewer
  - Lab reports viewer (file upload/download)
  - Appointment booking calendar
  - Symptom checker (self-service, non-diagnostic)

- [ ] **Shared Components**
  - Navigation bar
  - Footer
  - Loading spinners
  - Error handling UI
  - Responsive design (mobile-friendly)

#### Deliverables:
- Complete React.js frontend
- Doctor portal fully functional
- Patient portal fully functional
- Responsive UI design

---

### Phase 5: Integration & Testing (Week 12-14)

#### Tasks:
- [ ] **End-to-End Integration**
  - Connect frontend to backend APIs
  - Test authentication flow
  - Test ML prediction pipeline
  - Test drug suggestion system
  
- [ ] **Testing**
  - Unit tests for ML models
  - API endpoint tests
  - Frontend component tests
  - Integration tests
  - User acceptance testing with dummy data
  
- [ ] **Bug Fixes & Optimization**
  - Fix identified bugs
  - Optimize database queries
  - Improve ML prediction speed
  - Optimize frontend performance

#### Deliverables:
- Fully integrated system
- Test report
- Bug fix log

---

### Phase 6: Deployment & Documentation (Week 15-16)

#### Tasks:
- [ ] **Deployment Preparation**
  - Set up cloud server (AWS, Azure, or Heroku)
  - Configure production database
  - Set up environment variables
  - Configure Firebase for production
  
- [ ] **Deployment**
  - Deploy backend API
  - Deploy PostgreSQL database
  - Deploy React frontend (build and serve)
  - Configure domain and SSL certificates
  
- [ ] **Documentation**
  - User manual for doctors
  - User manual for patients
  - API documentation
  - System architecture documentation
  - Deployment guide
  - README.md with setup instructions

#### Deliverables:
- Live deployed application
- Complete documentation
- Final project report

---

## 📊 Key Technical Decisions Needed

1. **Backend Framework**: Flask (simpler) vs Django (more features)
   - Recommendation: Flask (easier to learn, lighter, good for APIs)

2. **Database**: PostgreSQL (as specified) - good choice for relational data

3. **Authentication**: Firebase (as specified) - handles security well

4. **ML Model Selection**: Train all 4, compare, use best performer

5. **Drug Suggestion Logic**:
   - Use DrugBank indication field
   - Match predicted disease with drug indications
   - Filter by approved/active drugs only

---

## 🔧 Development Environment Setup

### Required Tools:
- Python 3.8+ (for backend & ML)
- Node.js 16+ (for React frontend)
- PostgreSQL 12+
- Git (version control)
- VS Code / PyCharm (IDE)

### Required Python Packages:
```
flask (or django)
pandas
numpy
scikit-learn
xgboost
joblib
psycopg2 (PostgreSQL driver)
python-docx (for document processing)
openpyxl (for Excel files)
firebase-admin (Firebase SDK)
```

### Required Node.js Packages:
```
react
react-router-dom
axios
bootstrap
react-bootstrap
firebase (for client-side auth)
```

---

## 🚨 Important Considerations

1. **Medical Disclaimer**: System should clearly state it's not a replacement for professional medical advice

2. **Data Privacy**: 
   - Encrypt patient data
   - HIPAA compliance considerations (if applicable)
   - Secure authentication

3. **Model Accuracy**: 
   - Start with baseline models
   - Iterate and improve
   - Document limitations

4. **Scalability**: 
   - Design for future growth
   - Consider caching for drug database
   - Optimize ML prediction endpoints

---

## 📈 Success Metrics

- ML Model Accuracy: > 70% (realistic for symptom-based diagnosis)
- API Response Time: < 2 seconds for predictions
- System Uptime: > 95%
- User Satisfaction: Positive feedback from test users

---

## Next Steps

1. ✅ Review and approve this plan
2. Set up development environment
3. Begin Phase 1: Data preparation
4. Weekly progress reviews

---

**Project Timeline**: 16 weeks (as per proposal)
**Team Members**: 
- Muhammad Rehan Ishaq (Frontend & UI)
- Syed Farman Ali (Backend & AI)

**Last Updated**: Based on initial file review

