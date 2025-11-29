# Virtual Health Assistant - Frontend

React-based frontend application for the Virtual Health Assistant.

## 📋 Overview

This frontend provides user interfaces for:
- **Patient Portal**: View medical records, prescriptions, book appointments
- **Doctor Portal**: Manage patients, diagnose symptoms, create prescriptions
- **Authentication**: Secure login and registration with JWT

## 🛠️ Tech Stack

- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0
- **Routing**: React Router DOM 6.20
- **UI Framework**: Bootstrap 5.3 + React Bootstrap 2.9
- **HTTP Client**: Axios 1.6
- **Authentication**: JWT-based (no Firebase needed)
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
│   ├── services/         # API services
│   │   └── api.js        # Axios API client with JWT
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

**Check Node.js version:**

#### macOS/Linux:
```bash
node --version
```

#### Windows:
```cmd
node --version
```

**If not installed:**
- Download from [Node.js website](https://nodejs.org/)
- Run installer (Windows will handle PATH automatically)

### 2. Install Dependencies

#### macOS/Linux:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

#### Windows (Command Prompt):

```cmd
REM Navigate to frontend directory
cd frontend

REM Install dependencies
npm install

REM Or using yarn
yarn install
```

#### Windows (PowerShell):

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

### 3. Environment Configuration

#### macOS/Linux:

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API configuration
# Only need to set if backend is not on localhost:5000
```

#### Windows (Command Prompt):

```cmd
REM Copy environment template
copy .env.example .env

REM Edit .env file with your API configuration
REM Only need to set if backend is not on localhost:5000
```

#### Windows (PowerShell):

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env file with your API configuration
# Only need to set if backend is not on localhost:5000
```

**Required environment variables:**
- `VITE_API_BASE_URL` (optional, defaults to `/api`)

**Example `.env` file:**
```env
# Backend API URL (optional, defaults to /api)
# For local development, leave as /api (Vite proxy will handle it)
VITE_API_BASE_URL=/api

# For production or different backend URL:
# VITE_API_BASE_URL=http://localhost:5000/api
# VITE_API_BASE_URL=https://api.example.com/api
```

### 4. Run Development Server

#### macOS/Linux:

```bash
# Start development server
npm run dev

# Server will start on http://localhost:3000
# Vite will automatically proxy /api requests to backend at http://localhost:5000
```

#### Windows:

```cmd
REM Start development server
npm run dev

REM Server will start on http://localhost:3000
REM Vite will automatically proxy /api requests to backend at http://localhost:5000
```

### 5. Build for Production

#### macOS/Linux/Windows:

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
   - Automatically adds JWT token to requests
   - Handles token refresh on 401 errors
   - Handles errors globally

2. **API Helper Functions** (`src/services/api.js`)
   - `authAPI` - Authentication endpoints
   - `patientAPI` - Patient management
   - `doctorAPI` - Doctor management
   - `diagnosisAPI` - Disease prediction
   - `drugAPI` - Drug search and suggestions
   - `prescriptionAPI` - Prescription management
   - `appointmentAPI` - Appointment scheduling

## 🔐 Authentication Flow (JWT-based)

1. User registers/logs in with email and password
2. Frontend sends credentials to backend API
3. Backend validates and returns JWT tokens (access + refresh)
4. Frontend stores tokens in localStorage
5. API requests automatically include JWT token in Authorization header
6. When access token expires, frontend automatically refreshes it
7. User is redirected to login if refresh fails

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
- `axios` - HTTP client with JWT support
- `bootstrap` & `react-bootstrap` - UI framework
- `react-toastify` - Toast notifications

## 🚨 Important Notes

- **Environment Variables**: All env vars must be prefixed with `VITE_` to be accessible in the app
- **API Proxy**: Development server proxies `/api/*` to `http://localhost:5000` (backend)
- **CORS**: Backend must allow requests from frontend origin
- **JWT Tokens**: Stored in localStorage (consider httpOnly cookies for production)

## 🐛 Troubleshooting

### API Connection Issues

#### Check Backend is Running:
```bash
# macOS/Linux/Windows
# Verify backend server is running on port 5000
curl http://localhost:5000/api/auth/verify
```

#### Check CORS Settings:
- Verify backend allows requests from `http://localhost:3000`
- Check `CORS_ORIGINS` in backend `.env` file

#### Check API Base URL:
- Verify `VITE_API_BASE_URL` in frontend `.env`
- Default should be `/api` for development (uses Vite proxy)

### Build Issues

#### macOS/Linux:
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install

# Clear Vite cache
rm -rf .vite

# Check Node.js version
node --version  # Should be 16+
```

#### Windows (Command Prompt):
```cmd
REM Clear node_modules and reinstall
rmdir /s /q node_modules
npm install

REM Clear Vite cache
rmdir /s /q .vite

REM Check Node.js version
node --version  REM Should be 16+
```

#### Windows (PowerShell):
```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install

# Clear Vite cache
Remove-Item -Recurse -Force .vite

# Check Node.js version
node --version  # Should be 16+
```

### Port Already in Use

#### macOS/Linux:
```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

#### Windows:
```cmd
REM Find process using port 3000
netstat -ano | findstr :3000

REM Kill process (replace PID)
taskkill /PID <PID> /F
```

### JWT Token Issues

- **Token expired**: Frontend should automatically refresh, check console for errors
- **Token invalid**: Clear localStorage and login again
- **CORS errors**: Ensure backend allows frontend origin

### Module Not Found Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Windows:
rmdir /s /q node_modules
del package-lock.json
npm install
```

## 🪟 Windows-Specific Tips

1. **Use PowerShell** for better experience (better than Command Prompt)
2. **Path separators**: Use forward slashes `/` in code (Node.js handles both)
3. **Line endings**: Git should handle automatically, but use `core.autocrlf true`
4. **Long paths**: Enable long path support in Windows if issues arise
5. **Antivirus**: May slow down `npm install`, consider adding exception for project folder

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [JWT Authentication Guide](../JWT_AUTHENTICATION.md)

## 📞 Support

For issues or questions, refer to:
- Main project README: `../README.md`
- JWT Authentication guide: `../JWT_AUTHENTICATION.md`
- Quick Start guide: `../QUICK_START.md`
- Backend README: `../backend/README.md`
