/**
 * Root App — routes and auth guards.
 * Data flow: pages use services/api.js (JWT) → Flask /api/* (see docs/PROJECT_GUIDE.md).
 */

import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import 'bootstrap/dist/css/bootstrap.min.css'

// Import page components
import LoginPage from './pages/LoginPage'
import DoctorDashboard from './pages/DoctorDashboard'
import PatientDashboard from './pages/PatientDashboard'
import NotFound from './pages/NotFound'

// Import layout components
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'

// Import authentication context
import { AuthProvider, useAuth } from './context/AuthContext'

/**
 * Protected route component.
 * Redirects to login if user is not authenticated.
 */
function ProtectedRoute({ children, requiredRole = null }) {
  const { user, loading } = useAuth()
  
  // Show loading spinner while checking authentication
  if (loading) {
    return <div className="text-center p-5">Loading...</div>
  }
  
  // Redirect to login if not authenticated
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  // Check role if required
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" replace />
  }
  
  return children
}

/**
 * Main App component with routing.
 */
function AppContent() {
  return (
    <div className="App min-vh-100 d-flex flex-column">
      {/* Navigation bar */}
      <Navbar />
      
      {/* Main content area */}
      <main className="flex-grow-1">
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
          
          {/* Protected routes - Doctor */}
          <Route
            path="/doctor/dashboard"
            element={
              <ProtectedRoute requiredRole="doctor">
                <DoctorDashboard />
              </ProtectedRoute>
            }
          />
          
          {/* Protected routes - Patient */}
          <Route
            path="/patient/dashboard"
            element={
              <ProtectedRoute requiredRole="patient">
                <PatientDashboard />
              </ProtectedRoute>
            }
          />
          
          {/* 404 Not Found */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      
      {/* Footer */}
      <Footer />
      
      {/* Toast notifications container */}
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  )
}

/**
 * Root App component wrapped with AuthProvider.
 */
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

