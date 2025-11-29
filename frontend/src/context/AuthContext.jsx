/**
 * Authentication Context Provider.
 * 
 * Manages user authentication state and provides authentication methods.
 * Uses JWT (JSON Web Token) authentication with the backend API.
 */

import React, { createContext, useContext, useState, useEffect } from 'react'
import api, { authAPI } from '../services/api'

// Create authentication context
const AuthContext = createContext(null)

// Token storage keys
const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const USER_KEY = 'user'

/**
 * Authentication Provider component.
 * 
 * Provides authentication state and methods to child components.
 */
export function AuthProvider({ children }) {
  // Current user state
  const [user, setUser] = useState(null)
  
  // Loading state while checking authentication
  const [loading, setLoading] = useState(true)
  
  // Error state
  const [error, setError] = useState(null)
  
  /**
   * Check for stored authentication on mount.
   * If valid token exists, restore user session.
   */
  useEffect(() => {
    checkAuthStatus()
  }, [])
  
  /**
   * Check if user is authenticated by verifying stored token.
   */
  const checkAuthStatus = async () => {
    try {
      // Check for stored tokens
      const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY)
      
      if (!accessToken) {
        setLoading(false)
        return
      }
      
      // Set token in API interceptor
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
      
      // Try to get current user from backend
      const response = await authAPI.getCurrentUser()
      
      if (response.data) {
        // Get stored user data or use response data
        const storedUser = JSON.parse(localStorage.getItem(USER_KEY) || 'null')
        setUser(storedUser || response.data)
      } else {
        // Token invalid, clear storage
        clearAuth()
      }
    } catch (err) {
      // Token invalid or expired, clear storage
      console.error('Auth check failed:', err)
      clearAuth()
    } finally {
      setLoading(false)
    }
  }
  
  /**
   * Clear authentication data from storage and state.
   */
  const clearAuth = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    delete api.defaults.headers.common['Authorization']
    setUser(null)
  }
  
  /**
   * Sign in with email and password.
   * 
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} - Promise that resolves when sign in completes
   */
  const signIn = async (email, password) => {
    try {
      setError(null)
      
      // Call login API endpoint
      const response = await authAPI.login({ email, password })
      
      const { access_token, refresh_token, user: userData } = response.data
      
      // Store tokens and user data
      localStorage.setItem(ACCESS_TOKEN_KEY, access_token)
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token)
      localStorage.setItem(USER_KEY, JSON.stringify(userData))
      
      // Set authorization header for future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      // Update user state
      setUser(userData)
      
      return userData
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Login failed'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }
  
  /**
   * Sign up new user with email and password.
   * 
   * @param {string} email - User email
   * @param {string} password - User password
   * @param {string} role - User role ('patient' or 'doctor')
   * @returns {Promise} - Promise that resolves when sign up completes
   */
  const signUp = async (email, password, role = 'patient') => {
    try {
      setError(null)
      
      // Call register API endpoint
      const response = await authAPI.register({ email, password, role })
      
      const { access_token, refresh_token, user: userData } = response.data
      
      // Store tokens and user data
      localStorage.setItem(ACCESS_TOKEN_KEY, access_token)
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token)
      localStorage.setItem(USER_KEY, JSON.stringify(userData))
      
      // Set authorization header for future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      // Update user state
      setUser(userData)
      
      return userData
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Registration failed'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }
  
  /**
   * Sign out current user.
   * 
   * Clears tokens and user data from storage.
   * 
   * @returns {Promise} - Promise that resolves when sign out completes
   */
  const signOut = async () => {
    try {
      setError(null)
      
      // Call logout API endpoint (optional, for token blacklisting)
      try {
        await authAPI.logout()
      } catch (err) {
        // Logout API call failed, but continue with local logout
        console.warn('Logout API call failed:', err)
      }
      
      // Clear local storage and state
      clearAuth()
    } catch (err) {
      setError(err.message)
      // Even if logout fails, clear local data
      clearAuth()
      throw err
    }
  }
  
  /**
   * Refresh access token using refresh token.
   * 
   * Called automatically when access token expires.
   * 
   * @returns {Promise} - Promise that resolves with new access token
   */
  const refreshAccessToken = async () => {
    try {
      const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
      
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }
      
      // Set refresh token in header temporarily
      api.defaults.headers.common['Authorization'] = `Bearer ${refreshToken}`
      
      // Call refresh endpoint
      const response = await authAPI.refresh()
      
      const { access_token } = response.data
      
      // Store new access token
      localStorage.setItem(ACCESS_TOKEN_KEY, access_token)
      
      // Update authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      return access_token
    } catch (err) {
      // Refresh failed, clear auth and require re-login
      clearAuth()
      throw err
    }
  }
  
  // Value object to provide to context consumers
  const value = {
    user,
    loading,
    error,
    signIn,
    signUp,
    signOut,
    refreshAccessToken,
    isAuthenticated: !!user
  }
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

/**
 * Hook to access authentication context.
 * 
 * @returns {object} - Authentication context value
 * @throws {Error} - If used outside AuthProvider
 */
export function useAuth() {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  
  return context
}
