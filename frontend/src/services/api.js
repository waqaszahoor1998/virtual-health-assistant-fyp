/**
 * API service for backend communication.
 * 
 * This module provides a centralized axios instance configured
 * for communicating with the backend API using JWT authentication.
 */

import axios from 'axios'

// Base URL for backend API
// In development, Vite proxy will forward /api requests to backend
// In production, use full backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,  // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor to add authentication token.
 * 
 * Gets JWT token from localStorage and adds it to request headers.
 * Also handles token refresh on 401 errors.
 */
api.interceptors.request.use(
  async (config) => {
    try {
      // Get access token from localStorage
      const accessToken = localStorage.getItem('access_token')
      
      if (accessToken) {
        // Add token to Authorization header
        config.headers.Authorization = `Bearer ${accessToken}`
      }
    } catch (error) {
      console.error('Error setting auth token:', error)
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor to handle errors globally.
 * 
 * Handles common error cases like 401 (unauthorized) and automatically
 * attempts to refresh the access token.
 */
api.interceptors.response.use(
  (response) => {
    // Return response data directly
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // Try to refresh the access token
        const refreshToken = localStorage.getItem('refresh_token')
        
        if (refreshToken) {
          // Set refresh token in header
          api.defaults.headers.common['Authorization'] = `Bearer ${refreshToken}`
          
          // Call refresh endpoint
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
            headers: {
              'Authorization': `Bearer ${refreshToken}`
            }
          })
          
          const { access_token } = response.data
          
          // Store new access token
          localStorage.setItem('access_token', access_token)
          
          // Update authorization header
          originalRequest.headers['Authorization'] = `Bearer ${access_token}`
          
          // Retry original request with new token
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, clear auth and redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        delete api.defaults.headers.common['Authorization']
        
        // Redirect to login page
        window.location.href = '/login'
        
        return Promise.reject(refreshError)
      }
    }
    
    // Handle other error responses
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          // Bad request
          console.error('Bad request:', data?.error || error.message)
          break
        case 403:
          // Forbidden
          console.error('Forbidden - insufficient permissions')
          break
        case 404:
          // Not found
          console.error('Resource not found')
          break
        case 500:
          // Server error
          console.error('Server error')
          break
        default:
          console.error('API error:', data?.error || error.message)
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('No response from server')
    } else {
      // Error in request setup
      console.error('Request error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// Export API instance and helper methods
export default api

/**
 * API helper functions for common operations
 */

// Authentication endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  refresh: () => api.post('/auth/refresh'),
  verify: () => api.get('/auth/verify'),
  getCurrentUser: () => api.get('/auth/user'),
}

// Patient endpoints
export const patientAPI = {
  getAll: (params) => api.get('/patients', { params }),
  getById: (id) => api.get(`/patients/${id}`),
  create: (data) => api.post('/patients', data),
  update: (id, data) => api.put(`/patients/${id}`, data),
  delete: (id) => api.delete(`/patients/${id}`),
}

// Doctor endpoints
export const doctorAPI = {
  getAll: () => api.get('/doctors'),
  getById: (id) => api.get(`/doctors/${id}`),
}

// Diagnosis endpoints
export const diagnosisAPI = {
  predict: (symptoms, modelType = 'xgboost', topK = 5) => api.post('/diagnosis/predict', {
    symptoms,
    model_type: modelType,
    top_k: topK
  }),
  create: (data) => api.post('/diagnosis', data),
  getById: (id) => api.get(`/diagnosis/${id}`),
}

// Drug endpoints
export const drugAPI = {
  search: (query) => api.get('/drugs/search', { params: { q: query } }),
  suggest: (diagnosisId) => api.post('/drugs/suggest', { diagnosis_id: diagnosisId }),
}

// Prescription endpoints
export const prescriptionAPI = {
  create: (data) => api.post('/prescriptions', data),
  getById: (id) => api.get(`/prescriptions/${id}`),
  getByPatient: (patientId) => api.get(`/prescriptions/patient/${patientId}`),
}

// Appointment endpoints
export const appointmentAPI = {
  create: (data) => api.post('/appointments', data),
  getAll: () => api.get('/appointments'),
  getById: (id) => api.get(`/appointments/${id}`),
  update: (id, data) => api.put(`/appointments/${id}`, data),
  delete: (id) => api.delete(`/appointments/${id}`),
}
