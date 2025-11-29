/**
 * Appointment Booking Modal Component.
 * 
 * Allows patients to book appointments with doctors.
 * Shows available doctors, date/time picker, and reason input.
 * 
 * Features:
 * - Doctor selection
 * - Date and time picker
 * - Reason for appointment
 * - Form validation
 * - API integration
 */

import React, { useState, useEffect } from 'react'
import { Modal, Form, Button, Alert, Spinner } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { appointmentAPI, doctorAPI, patientAPI } from '../services/api'

/**
 * AppointmentBookingModal Component
 * 
 * @param {boolean} show - Whether modal is visible
 * @param {Function} onHide - Callback to close modal
 * @param {Function} onSuccess - Callback when appointment is created successfully
 * @param {number} selectedDoctorId - Pre-selected doctor ID (optional)
 */
function AppointmentBookingModal({ show, onHide, onSuccess, selectedDoctorId = null }) {
  // Form state
  const [doctorId, setDoctorId] = useState(selectedDoctorId || '')
  const [appointmentDate, setAppointmentDate] = useState('')
  const [appointmentTime, setAppointmentTime] = useState('')
  const [reason, setReason] = useState('')
  const [notes, setNotes] = useState('')
  
  // Loading states
  const [loadingDoctors, setLoadingDoctors] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  
  // Data
  const [doctors, setDoctors] = useState([])
  const [patientId, setPatientId] = useState(null)
  const [errors, setErrors] = useState({})
  
  /**
   * Load doctors list and patient info when modal opens.
   */
  useEffect(() => {
    if (show) {
      loadDoctors()
      loadPatientInfo()
      // Set default date to tomorrow
      const tomorrow = new Date()
      tomorrow.setDate(tomorrow.getDate() + 1)
      setAppointmentDate(tomorrow.toISOString().split('T')[0])
      setAppointmentTime('09:00')
    }
  }, [show, selectedDoctorId])
  
  /**
   * Load patient info to get patient_id.
   */
  const loadPatientInfo = async () => {
    try {
      const response = await patientAPI.getAll()
      if (response.data.patients && response.data.patients.length > 0) {
        setPatientId(response.data.patients[0].id)
      }
    } catch (error) {
      console.error('Error loading patient info:', error)
      toast.error('Failed to load patient information')
    }
  }
  
  /**
   * Load available doctors.
   */
  const loadDoctors = async () => {
    setLoadingDoctors(true)
    try {
      const response = await doctorAPI.getAll()
      setDoctors(response.data.doctors || [])
      
      // Pre-select doctor if provided
      if (selectedDoctorId) {
        setDoctorId(selectedDoctorId)
      }
    } catch (error) {
      console.error('Error loading doctors:', error)
      toast.error('Failed to load doctors. Please try again.')
    } finally {
      setLoadingDoctors(false)
    }
  }
  
  /**
   * Validate form data.
   */
  const validateForm = () => {
    const newErrors = {}
    
    if (!doctorId) {
      newErrors.doctorId = 'Please select a doctor'
    }
    
    if (!appointmentDate) {
      newErrors.appointmentDate = 'Please select a date'
    } else {
      const selectedDate = new Date(`${appointmentDate}T${appointmentTime || '00:00'}`)
      const now = new Date()
      if (selectedDate <= now) {
        newErrors.appointmentDate = 'Appointment date must be in the future'
      }
    }
    
    if (!appointmentTime) {
      newErrors.appointmentTime = 'Please select a time'
    }
    
    if (!reason.trim()) {
      newErrors.reason = 'Please provide a reason for the appointment'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }
  
  /**
   * Handle form submission.
   */
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      toast.error('Please fix the errors in the form')
      return
    }
    
    setSubmitting(true)
    
    try {
      if (!patientId) {
        toast.error('Patient information not loaded. Please try again.')
        return
      }
      
      // Combine date and time
      const appointmentDateTime = `${appointmentDate}T${appointmentTime}:00`
      
      const appointmentData = {
        patient_id: patientId,
        doctor_id: parseInt(doctorId),
        appointment_date: appointmentDateTime,
        reason: reason.trim(),
        notes: notes.trim() || undefined
      }
      
      // Note: patient_id should come from authenticated user's profile
      // This will need to be fetched from patient profile
      // For now, we'll need to get it from the API or context
      
      const response = await appointmentAPI.create(appointmentData)
      
      if (response.data) {
        toast.success('Appointment booked successfully!')
        
        // Reset form
        resetForm()
        
        // Close modal and notify parent
        onHide()
        if (onSuccess) {
          onSuccess(response.data.appointment)
        }
      }
    } catch (error) {
      console.error('Error booking appointment:', error)
      const errorMessage = error.response?.data?.error || 'Failed to book appointment. Please try again.'
      toast.error(errorMessage)
      
      // Show specific validation errors if available
      if (error.response?.data?.errors) {
        setErrors(error.response.data.errors)
      }
    } finally {
      setSubmitting(false)
    }
  }
  
  /**
   * Reset form to initial state.
   */
  const resetForm = () => {
    setDoctorId(selectedDoctorId || '')
    setAppointmentDate('')
    setAppointmentTime('')
    setReason('')
    setNotes('')
    setErrors({})
  }
  
  /**
   * Handle modal close.
   */
  const handleClose = () => {
    resetForm()
    onHide()
  }
  
  /**
   * Generate time slots for selection.
   */
  const generateTimeSlots = () => {
    const slots = []
    for (let hour = 9; hour <= 17; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const timeString = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`
        slots.push(timeString)
      }
    }
    return slots
  }
  
  /**
   * Get minimum date for date picker (tomorrow).
   */
  const getMinDate = () => {
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    return tomorrow.toISOString().split('T')[0]
  }
  
  return (
    <Modal show={show} onHide={handleClose} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>Book Appointment</Modal.Title>
      </Modal.Header>
      
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          {/* Doctor Selection */}
          <Form.Group className="mb-3">
            <Form.Label>
              Select Doctor <span className="text-danger">*</span>
            </Form.Label>
            {loadingDoctors ? (
              <div className="text-center py-3">
                <Spinner animation="border" size="sm" />
                <span className="ms-2">Loading doctors...</span>
              </div>
            ) : (
              <Form.Select
                value={doctorId}
                onChange={(e) => setDoctorId(e.target.value)}
                isInvalid={!!errors.doctorId}
              >
                <option value="">-- Select a doctor --</option>
                {doctors.map((doctor) => (
                  <option key={doctor.id} value={doctor.id}>
                    Dr. {doctor.first_name} {doctor.last_name}
                    {doctor.specialization && ` - ${doctor.specialization}`}
                  </option>
                ))}
              </Form.Select>
            )}
            {errors.doctorId && (
              <Form.Control.Feedback type="invalid">
                {errors.doctorId}
              </Form.Control.Feedback>
            )}
          </Form.Group>
          
          {/* Date Selection */}
          <Form.Group className="mb-3">
            <Form.Label>
              Appointment Date <span className="text-danger">*</span>
            </Form.Label>
            <Form.Control
              type="date"
              value={appointmentDate}
              onChange={(e) => setAppointmentDate(e.target.value)}
              min={getMinDate()}
              isInvalid={!!errors.appointmentDate}
            />
            {errors.appointmentDate && (
              <Form.Control.Feedback type="invalid">
                {errors.appointmentDate}
              </Form.Control.Feedback>
            )}
          </Form.Group>
          
          {/* Time Selection */}
          <Form.Group className="mb-3">
            <Form.Label>
              Appointment Time <span className="text-danger">*</span>
            </Form.Label>
            <Form.Select
              value={appointmentTime}
              onChange={(e) => setAppointmentTime(e.target.value)}
              isInvalid={!!errors.appointmentTime}
            >
              <option value="">-- Select time --</option>
              {generateTimeSlots().map((time) => (
                <option key={time} value={time}>
                  {new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: true
                  })}
                </option>
              ))}
            </Form.Select>
            {errors.appointmentTime && (
              <Form.Control.Feedback type="invalid">
                {errors.appointmentTime}
              </Form.Control.Feedback>
            )}
          </Form.Group>
          
          {/* Reason */}
          <Form.Group className="mb-3">
            <Form.Label>
              Reason for Appointment <span className="text-danger">*</span>
            </Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="Describe the reason for your appointment..."
              isInvalid={!!errors.reason}
            />
            {errors.reason && (
              <Form.Control.Feedback type="invalid">
                {errors.reason}
              </Form.Control.Feedback>
            )}
          </Form.Group>
          
          {/* Notes (Optional) */}
          <Form.Group className="mb-3">
            <Form.Label>Additional Notes (Optional)</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Any additional information you'd like to share..."
            />
          </Form.Group>
          
          {/* Info Alert */}
          <Alert variant="info" className="mb-0">
            <small>
              <strong>Note:</strong> Your appointment request will be reviewed and confirmed by the doctor.
              You will be notified once it's confirmed.
            </small>
          </Alert>
        </Modal.Body>
        
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose} disabled={submitting}>
            Cancel
          </Button>
          <Button variant="primary" type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                  className="me-2"
                />
                Booking...
              </>
            ) : (
              'Book Appointment'
            )}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  )
}

export default AppointmentBookingModal

