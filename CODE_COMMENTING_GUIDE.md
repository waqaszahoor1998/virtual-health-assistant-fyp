# Code Commenting Guide

## Overview

This document outlines the commenting standards used throughout the Virtual Health Assistant project. All code files follow comprehensive commenting practices to ensure code maintainability and understanding.

## Comment Standards

### Python Files (.py)

#### File Header
Every Python file should start with:
- Module docstring explaining the file's purpose
- Brief description of main functionality
- List of key classes/functions

#### Class Documentation
Every class should have:
- Comprehensive docstring with description
- Attributes section listing all attributes
- Relationships section (for models)
- Example usage

#### Function/Method Documentation
Every function should have:
- Purpose description
- Args section with type and description
- Returns section with type and description
- Raises section (if applicable)
- Example usage for complex functions

#### Inline Comments
- Complex logic blocks should have explanatory comments
- Non-obvious code should be explained
- Algorithm steps should be documented

### JavaScript/JSX Files (.js, .jsx)

#### File Header
Every file should start with:
- JSDoc-style comment explaining the file's purpose
- Brief description of main functionality

#### Component Documentation
Every React component should have:
- Component purpose description
- Props documentation with types
- State variables explained
- Key functionality described

#### Function Documentation
Every function should have:
- JSDoc comment with description
- @param tags for parameters
- @returns tag for return value
- @throws tag for exceptions

## Status

✅ **Completed:**
- Backend models (User, Patient, Doctor, Diagnosis, Prescription, Appointment)
- Backend APIs (Auth, Patients, Doctors, Diagnosis, Drugs)
- Backend utilities (ML Service, DrugBank Service)
- Frontend components (SymptomSelector, DiseasePredictionCard)
- Frontend pages (LoginPage, Dashboards)
- Frontend services (API service, Auth Context)
- ML scripts (Feature Engineering, Training scripts)

🔄 **In Progress:**
- Additional model files (Drug, Disease, Symptom)
- Additional API files (Prescriptions, Appointments)
- Additional frontend components
- Additional utility scripts

## Examples

See any enhanced file in the codebase for examples of comprehensive commenting.

