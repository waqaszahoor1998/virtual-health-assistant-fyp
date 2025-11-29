# Virtual Health Assistant - Frontend

React-based frontend application for the Virtual Health Assistant.

## 📋 Overview

This frontend provides user interfaces for:
- **Patient Portal**: View medical records, prescriptions, book appointments
- **Doctor Portal**: Manage patients, diagnose symptoms, create prescriptions
- **Authentication**: Secure login and registration with Firebase

## 🛠️ Tech Stack

- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0
- **Routing**: React Router DOM 6.20
- **UI Framework**: Bootstrap 5.3 + React Bootstrap 2.9
- **HTTP Client**: Axios 1.6
- **Authentication**: Firebase Auth 10.7
- **Notifications**: React Toastify 9.1

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable components
│   │   └── layout/       # Layout components (Navbar, Footer)
│   ├── pages/            # Page components
│   │   ├── LoginPage.jsx
│   │   ├── DoctorDashboard.jsx
│   │   ├── PatientDashboard.jsx
│   │   └── NotFound.jsx
│   ├── context/          # React Context providers
│   │   └── AuthContext.jsx
│   ├── services/         # API and external services
│   │   ├── api.js        # Axios API client
│   │   └── firebase.js   # Firebase configuration
│   ├── utils/            # Utility functions
│   ├── assets/           # Images, fonts, etc.
│   ├── App.jsx           # Root App component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── package.json          # Dependencies
├── vite.config.js        # Vite configuration
└── .env.example         # Environment variables template
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Node.js 16 or higher
- npm or yarn package manager

### 2. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Firebase configuration
# Get Firebase config from Firebase Console > Project Settings > Your apps
```

Required environment variables:
- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_STORAGE_BUCKET`
- `VITE_FIREBASE_MESSAGING_SENDER_ID`
- `VITE_FIREBASE_APP_ID`
- `VITE_API_BASE_URL` (optional, defaults to `/api`)

### 4. Run Development Server

```bash
# Start development server
npm run dev

# Server will start on http://localhost:3000
# Vite will automatically proxy /api requests to backend at http://localhost:5000
```

### 5. Build for Production

```bash
# Build production bundle
npm run build

# Preview production build
npm run preview
```

## 📡 API Integration

The frontend communicates with the backend API through:

1. **Axios Instance** (`src/services/api.js`)
   - Configured with base URL and interceptors
   - Automatically adds Firebase auth token to requests
   - Handles errors globally

2. **API Helper Functions** (`src/services/api.js`)
   - `authAPI` - Authentication endpoints
   - `patientAPI` - Patient management
   - `doctorAPI` - Doctor management
   - `diagnosisAPI` - Disease prediction
   - `drugAPI` - Drug search and suggestions
   - `prescriptionAPI` - Prescription management
   - `appointmentAPI` - Appointment scheduling

## 🔐 Authentication Flow

1. User signs in/up with Firebase Auth
2. Firebase returns user credential with ID token
3. Frontend stores user in AuthContext
4. API requests automatically include Firebase ID token
5. Backend verifies token and returns user profile

## 📱 Pages

### Login Page (`/login`)
- User authentication (login/signup)
- Role selection (patient/doctor)
- Form validation

### Doctor Dashboard (`/doctor/dashboard`)
- Patient list
- Upcoming appointments
- Quick actions (diagnosis, prescriptions)

### Patient Dashboard (`/patient/dashboard`)
- Medical history
- Upcoming appointments
- Prescriptions list
- Appointment booking

### 404 Not Found
- Shown for invalid routes

## 🎨 Styling

- **Bootstrap 5**: Responsive grid system and components
- **React Bootstrap**: Bootstrap components for React
- **Custom CSS**: Global styles and theme variables in `index.css`

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 📦 Key Dependencies

- `react` - UI library
- `react-router-dom` - Client-side routing
- `axios` - HTTP client
- `firebase` - Firebase SDK for authentication
- `bootstrap` & `react-bootstrap` - UI framework
- `react-toastify` - Toast notifications

## 🚨 Important Notes

- **Environment Variables**: All env vars must be prefixed with `VITE_` to be accessible in the app
- **API Proxy**: Development server proxies `/api/*` to `http://localhost:5000` (backend)
- **Firebase Setup**: Must configure Firebase project before running
- **CORS**: Backend must allow requests from frontend origin

## 🐛 Troubleshooting

### Firebase Configuration Issues
- Ensure all Firebase env variables are set in `.env`
- Verify Firebase project settings in Firebase Console
- Check Firebase Authentication is enabled

### API Connection Issues
- Verify backend server is running on port 5000
- Check CORS settings in backend
- Verify API base URL in `.env`

### Build Issues
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf .vite`
- Check Node.js version: `node --version` (should be 16+)

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Bootstrap Documentation](https://getbootstrap.com/)

