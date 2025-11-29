# Testing Guide - Virtual Health Assistant

## Overview

This guide provides comprehensive testing instructions for the Virtual Health Assistant application. It covers manual testing procedures, test data setup, and expected behaviors.

## Prerequisites

Before testing, ensure:
- ✅ Backend server is running (`python backend/run.py`)
- ✅ Frontend server is running (`npm run dev` in `frontend/`)
- ✅ Database is set up and migrations are applied
- ✅ ML models are trained (for diagnosis prediction)
- ✅ Test users are created

---

## Test Data Setup

### 1. Create Test Users

Use the registration API or frontend to create test accounts:

#### Doctor Account
- **Email**: `doctor@test.com`
- **Password**: `test123456`
- **Role**: `doctor`

#### Patient Account
- **Email**: `patient@test.com`
- **Password**: `test123456`
- **Role**: `patient`

### 2. Create Patient Profile

After registering as a patient, create a patient profile:
- First Name: `John`
- Last Name: `Doe`
- Phone: `+1234567890`
- Blood Type: `O+`
- Allergies: `Peanuts, Penicillin`

### 3. Create Doctor Profile

After registering as a doctor, create a doctor profile:
- First Name: `Jane`
- Last Name: `Smith`
- Specialization: `General Practice`
- License Number: `MD12345`
- Hospital/Clinic: `City Hospital`

---

## Manual Testing Checklist

### 🔐 Authentication Tests

#### Test 1: User Registration
- [ ] Navigate to `/login`
- [ ] Click "Sign Up" tab
- [ ] Fill in registration form:
  - Email: `test@example.com`
  - Password: `password123`
  - Role: Select `patient` or `doctor`
- [ ] Click "Sign Up"
- [ ] **Expected**: Success message, redirected to dashboard
- [ ] **Verify**: User can access dashboard

#### Test 2: User Login
- [ ] Navigate to `/login`
- [ ] Enter credentials:
  - Email: `doctor@test.com`
  - Password: `test123456`
- [ ] Click "Login"
- [ ] **Expected**: Redirected to doctor dashboard
- [ ] **Verify**: JWT token stored in localStorage

#### Test 3: Invalid Credentials
- [ ] Try logging in with wrong password
- [ ] **Expected**: Error message displayed
- [ ] **Verify**: Not redirected to dashboard

#### Test 4: Token Refresh
- [ ] Login successfully
- [ ] Wait for token expiration (or manually expire)
- [ ] Make API request
- [ ] **Expected**: Token automatically refreshed
- [ ] **Verify**: Request succeeds with new token

---

### 👨‍⚕️ Doctor Dashboard Tests

#### Test 5: View Patient List
- [ ] Login as doctor
- [ ] Navigate to "Patients" tab
- [ ] **Expected**: List of all patients displayed
- [ ] **Verify**: Patient names, phone numbers visible

#### Test 6: Search Patients
- [ ] In Patients tab, type search term in search box
- [ ] **Expected**: Filtered results shown
- [ ] **Verify**: Only matching patients displayed

#### Test 7: Select Patient for Diagnosis
- [ ] Click "Select for Diagnosis" on any patient
- [ ] **Expected**: 
  - Redirected to "Diagnosis" tab
  - Patient name displayed
  - Selected patient highlighted
- [ ] **Verify**: Patient selected state persists

#### Test 8: Symptom Selection
- [ ] In Diagnosis tab, select symptoms:
  - Use symptom selector to add symptoms
  - Try adding custom symptoms
- [ ] **Expected**: 
  - Symptoms appear as badges
  - Can remove symptoms
  - Maximum limit enforced (15 symptoms)
- [ ] **Verify**: Selected symptoms displayed correctly

#### Test 9: ML Disease Prediction
- [ ] Select at least 3 symptoms
- [ ] Click "Predict Diseases" button
- [ ] **Expected**: 
  - Loading spinner shown
  - Predictions displayed with confidence scores
  - Progress bars for confidence levels
  - Medical disclaimer visible
- [ ] **Verify**: 
  - Predictions are relevant to symptoms
  - Confidence scores between 0-100%
  - Top prediction highlighted

#### Test 10: Create Diagnosis
- [ ] After getting predictions:
  - Select/enter confirmed disease
  - Add clinical notes
- [ ] Click "Save Diagnosis"
- [ ] **Expected**: 
  - Success message
  - Form reset
  - Diagnosis saved to database
- [ ] **Verify**: Diagnosis appears in patient history

#### Test 11: View Appointments
- [ ] Navigate to "Appointments" tab
- [ ] **Expected**: List of appointments displayed
- [ ] **Verify**: 
  - Date/time formatted correctly
  - Status badges visible
  - Can view appointment details

---

### 👤 Patient Dashboard Tests

#### Test 12: View Profile
- [ ] Login as patient
- [ ] Navigate to "Overview" tab
- [ ] **Expected**: 
  - Profile information displayed
  - Quick stats visible
  - Quick action buttons shown
- [ ] **Verify**: All patient data accurate

#### Test 13: View Prescriptions
- [ ] Navigate to "Prescriptions" tab
- [ ] **Expected**: List of all prescriptions
- [ ] **Verify**: 
  - Drug names displayed
  - Dosage, frequency, duration shown
  - Instructions visible
  - Date formatted correctly

#### Test 14: View Appointments
- [ ] Navigate to "Appointments" tab
- [ ] **Expected**: List of patient appointments
- [ ] **Verify**: 
  - Upcoming appointments shown
  - Past appointments visible
  - Status badges correct

#### Test 15: Book Appointment
- [ ] Click "+ Request Appointment" button
- [ ] In modal:
  - Select doctor
  - Select date (future date)
  - Select time
  - Enter reason
  - Add optional notes
- [ ] Click "Book Appointment"
- [ ] **Expected**: 
  - Success message
  - Modal closes
  - Appointment appears in list
- [ ] **Verify**: Appointment status is "scheduled"

#### Test 16: Cancel Appointment
- [ ] Find a scheduled appointment
- [ ] Click "Cancel" button
- [ ] **Expected**: 
  - Confirmation dialog (if implemented)
  - Appointment status changes to "cancelled"
- [ ] **Verify**: Appointment updated in database

#### Test 17: View Medical History
- [ ] Navigate to "Medical History" tab
- [ ] **Expected**: List of past diagnoses
- [ ] **Verify**: 
  - Disease names shown
  - Dates displayed
  - Notes visible

---

### 🔍 API Integration Tests

#### Test 18: Backend API Health Check
```bash
curl http://localhost:5000/api/auth/verify
```
- [ ] **Expected**: Returns authentication status
- [ ] **Verify**: API responding correctly

#### Test 19: ML Prediction API
```bash
curl -X POST http://localhost:5000/api/diagnosis/predict \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "headache"], "top_k": 5}'
```
- [ ] **Expected**: Returns disease predictions
- [ ] **Verify**: 
  - Predictions array returned
  - Confidence scores between 0-1
  - Diseases are relevant

#### Test 20: Drug Search API
```bash
curl -X GET "http://localhost:5000/api/drugs/search?q=aspirin" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
- [ ] **Expected**: Returns matching drugs
- [ ] **Verify**: Results contain "aspirin" or related drugs

---

## Error Handling Tests

#### Test 21: Network Error Handling
- [ ] Disconnect internet
- [ ] Try to make API request
- [ ] **Expected**: Error message displayed
- [ ] **Verify**: App doesn't crash

#### Test 22: Invalid Form Data
- [ ] Try to submit forms with missing required fields
- [ ] **Expected**: 
  - Validation errors shown
  - Form not submitted
- [ ] **Verify**: Error messages are helpful

#### Test 23: Unauthorized Access
- [ ] Try to access doctor endpoints as patient
- [ ] **Expected**: 403 Forbidden error
- [ ] **Verify**: Appropriate error message

---

## Performance Tests

#### Test 24: Large Dataset Handling
- [ ] Load patient list with 100+ patients
- [ ] **Expected**: 
  - Pagination works
  - Page loads within 2 seconds
- [ ] **Verify**: No performance issues

#### Test 25: ML Prediction Speed
- [ ] Test prediction with 10 symptoms
- [ ] **Expected**: 
  - Response within 5 seconds
  - Loading state shown during wait
- [ ] **Verify**: User experience is smooth

---

## Browser Compatibility Tests

Test the application in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

**Verify**: All features work correctly in all browsers

---

## Security Tests

#### Test 26: XSS Protection
- [ ] Try to inject script tags in form fields
- [ ] **Expected**: Input sanitized
- [ ] **Verify**: No scripts executed

#### Test 27: SQL Injection
- [ ] Try SQL injection in search fields
- [ ] **Expected**: Input properly escaped
- [ ] **Verify**: No database errors

#### Test 28: JWT Token Security
- [ ] Check JWT token in localStorage
- [ ] **Expected**: 
  - Token is encrypted
  - Expires after set time
- [ ] **Verify**: Cannot be easily tampered with

---

## Known Issues & Limitations

### Current Limitations:
1. **ML Model Accuracy**: Model has low exact-match accuracy (~7%) due to small dataset
2. **Patient ID in Booking**: Appointment booking may need patient ID fetch fix
3. **No Real-time Updates**: Appointments/diagnoses don't update in real-time
4. **No Email Notifications**: Appointment confirmations not sent via email

### Areas for Improvement:
- Add unit tests for backend
- Add integration tests
- Add E2E tests with Cypress/Playwright
- Improve error messages
- Add loading skeletons
- Add optimistic UI updates

---

## Test Results Template

Use this template to track test results:

```
Test #: [Number]
Test Name: [Name]
Date: [Date]
Tester: [Name]
Status: ✅ Pass / ❌ Fail / ⚠️ Partial
Notes: [Any observations]
Screenshots: [If applicable]
```

---

## Automated Testing (Future)

### Backend Unit Tests
```bash
cd backend
pytest tests/
```

### Frontend Component Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
npm run test:e2e
```

---

## Reporting Issues

When reporting bugs, include:
1. Test number and name
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Browser/OS information
6. Screenshots if applicable
7. Console errors (if any)

---

## Quick Test Summary

**Critical Path Testing** (Must Pass):
1. ✅ User registration and login
2. ✅ Doctor can view patients
3. ✅ Doctor can create diagnosis with ML predictions
4. ✅ Patient can view prescriptions
5. ✅ Patient can book appointments

**Secondary Features** (Should Pass):
6. ✅ Search functionality
7. ✅ Form validation
8. ✅ Error handling
9. ✅ Loading states

**Nice-to-Have** (Optional):
10. ✅ Advanced filtering
11. ✅ Export features
12. ✅ Notifications

---

**Last Updated**: [Current Date]
**Tested By**: [Your Name]
**Version**: 1.0.0

