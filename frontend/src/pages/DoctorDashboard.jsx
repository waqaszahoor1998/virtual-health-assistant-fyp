/**
 * Doctor Dashboard Page.
 * 
 * Main dashboard for doctors with comprehensive functionality:
 * - Diagnosis interface with ML predictions
 * - Patient list and search
 * - Appointment management
 * - Quick actions and overview
 * 
 * Features:
 * - Symptom-based disease prediction using ML models
 * - Patient selection for creating diagnoses
 * - View and manage appointments
 * - Search and filter patients
 */

import React, { useState, useEffect } from 'react'
import { Container, Row, Col, Card, Tab, Tabs, Button, Alert, Spinner } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { useAuth } from '../context/AuthContext'
import { patientAPI, diagnosisAPI, appointmentAPI } from '../services/api'
import SymptomSelector from '../components/SymptomSelector'
import DiseasePredictionCard from '../components/DiseasePredictionCard'

/**
 * Main Doctor Dashboard component.
 */
function DoctorDashboard() {
  // Authentication context
  const { user } = useAuth()
  
  // Active tab state
  const [activeTab, setActiveTab] = useState('diagnosis')
  
  // ==================== DIAGNOSIS TAB STATE ====================
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [selectedSymptoms, setSelectedSymptoms] = useState([])
  const [predictions, setPredictions] = useState([])
  const [predicting, setPredicting] = useState(false)
  const [confirmingDiagnosis, setConfirmingDiagnosis] = useState(false)
  const [confirmedDisease, setConfirmedDisease] = useState('')
  const [diagnosisNotes, setDiagnosisNotes] = useState('')
  
  // ==================== PATIENTS TAB STATE ====================
  const [patients, setPatients] = useState([])
  const [loadingPatients, setLoadingPatients] = useState(false)
  const [patientSearch, setPatientSearch] = useState('')
  
  // ==================== APPOINTMENTS TAB STATE ====================
  const [appointments, setAppointments] = useState([])
  const [loadingAppointments, setLoadingAppointments] = useState(false)
  
  // Common symptoms list (can be loaded from API later)
  const commonSymptoms = [
    'fever', 'headache', 'cough', 'nausea', 'fatigue', 'dizziness',
    'chest pain', 'abdominal pain', 'back pain', 'joint pain',
    'shortness of breath', 'rash', 'sore throat', 'muscle pain',
    'diarrhea', 'vomiting', 'loss of appetite', 'weight loss',
    'insomnia', 'anxiety', 'depression', 'memory loss'
  ]
  
  /**
   * Load patients list on component mount and when tab changes.
   */
  useEffect(() => {
    if (activeTab === 'patients') {
      loadPatients()
    }
  }, [activeTab, patientSearch])
  
  /**
   * Load appointments on component mount and when tab changes.
   */
  useEffect(() => {
    if (activeTab === 'appointments') {
      loadAppointments()
    }
  }, [activeTab])
  
  /**
   * Load patients from API with search functionality.
   */
  const loadPatients = async () => {
    setLoadingPatients(true)
    try {
      const params = patientSearch ? { search: patientSearch } : {}
      const response = await patientAPI.getAll(params)
      setPatients(response.data.patients || [])
    } catch (error) {
      console.error('Error loading patients:', error)
      toast.error('Failed to load patients. Please try again.')
    } finally {
      setLoadingPatients(false)
    }
  }
  
  /**
   * Load appointments from API.
   */
  const loadAppointments = async () => {
    setLoadingAppointments(true)
    try {
      const response = await appointmentAPI.getAll()
      setAppointments(response.data.appointments || [])
    } catch (error) {
      console.error('Error loading appointments:', error)
      toast.error('Failed to load appointments. Please try again.')
    } finally {
      setLoadingAppointments(false)
    }
  }
  
  /**
   * Handle symptom selection change.
   */
  const handleSymptomsChange = (newSymptoms) => {
    setSelectedSymptoms(newSymptoms)
    // Clear predictions when symptoms change
    setPredictions([])
  }
  
  /**
   * Predict diseases from selected symptoms using ML model.
   */
  const handlePredict = async () => {
    if (selectedSymptoms.length === 0) {
      toast.warning('Please select at least one symptom')
      return
    }
    
    setPredicting(true)
    setPredictions([])
    
    try {
      const response = await diagnosisAPI.predict(selectedSymptoms, 'xgboost', 5)
      
      if (response.data.success && response.data.prediction) {
        setPredictions(response.data.prediction.predictions || [])
        toast.success('Disease prediction completed!')
      } else {
        toast.error('Prediction failed. Please try again.')
      }
    } catch (error) {
      console.error('Prediction error:', error)
      const errorMessage = error.response?.data?.error || 'Failed to predict diseases. Please try again.'
      toast.error(errorMessage)
    } finally {
      setPredicting(false)
    }
  }
  
  /**
   * Handle disease selection from predictions.
   */
  const handleDiseaseSelect = (diseaseName) => {
    setConfirmedDisease(diseaseName)
    toast.info(`Selected ${diseaseName} as confirmed diagnosis`)
  }
  
  /**
   * Create diagnosis record with confirmed disease.
   */
  const handleCreateDiagnosis = async () => {
    if (!selectedPatient) {
      toast.warning('Please select a patient first')
      return
    }
    
    if (selectedSymptoms.length === 0) {
      toast.warning('Please select symptoms')
      return
    }
    
    if (!confirmedDisease) {
      toast.warning('Please select or enter a confirmed disease')
      return
    }
    
    setConfirmingDiagnosis(true)
    
    try {
      const diagnosisData = {
        patient_id: selectedPatient.id,
        symptoms: selectedSymptoms,
        predicted_diseases: predictions,
        confirmed_disease: confirmedDisease,
        notes: diagnosisNotes
      }
      
      const response = await diagnosisAPI.create(diagnosisData)
      
      if (response.data) {
        toast.success('Diagnosis created successfully!')
        // Reset form
        setSelectedSymptoms([])
        setPredictions([])
        setConfirmedDisease('')
        setDiagnosisNotes('')
        setSelectedPatient(null)
      }
    } catch (error) {
      console.error('Error creating diagnosis:', error)
      const errorMessage = error.response?.data?.error || 'Failed to create diagnosis. Please try again.'
      toast.error(errorMessage)
    } finally {
      setConfirmingDiagnosis(false)
    }
  }
  
  /**
   * Format date for display.
   */
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  return (
    <Container fluid className="py-4">
      {/* Dashboard Header */}
      <Row className="mb-4">
        <Col>
          <h1 className="mb-1">Doctor Dashboard</h1>
          <p className="text-muted">Welcome back, {user?.email || 'Doctor'}</p>
        </Col>
      </Row>
      
      {/* Main Content Tabs */}
      <Tabs
        activeKey={activeTab}
        onSelect={(k) => setActiveTab(k)}
        className="mb-4"
      >
        {/* ==================== DIAGNOSIS TAB ==================== */}
        <Tab eventKey="diagnosis" title="Diagnosis">
          <Row>
            <Col lg={12}>
              <Card className="mb-4">
                <Card.Header>
                  <Card.Title className="mb-0">Create New Diagnosis</Card.Title>
                </Card.Header>
                <Card.Body>
                  {/* Patient Selection */}
                  <div className="mb-4">
                    <label className="form-label fw-bold">Select Patient</label>
                    {selectedPatient ? (
                      <div className="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                        <div>
                          <strong>{selectedPatient.first_name} {selectedPatient.last_name}</strong>
                          {selectedPatient.phone && (
                            <span className="text-muted ms-2">• {selectedPatient.phone}</span>
                          )}
                        </div>
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          onClick={() => setSelectedPatient(null)}
                        >
                          Change
                        </Button>
                      </div>
                    ) : (
                      <Alert variant="info" className="mb-0">
                        <Button
                          variant="link"
                          className="p-0 text-decoration-none"
                          onClick={() => setActiveTab('patients')}
                        >
                          Select a patient from the Patients tab
                        </Button>
                      </Alert>
                    )}
                  </div>
                  
                  {/* Symptom Selector */}
                  <div className="mb-4">
                    <label className="form-label fw-bold">Symptoms</label>
                    <SymptomSelector
                      selectedSymptoms={selectedSymptoms}
                      onSymptomsChange={handleSymptomsChange}
                      availableSymptoms={commonSymptoms}
                      maxSymptoms={15}
                    />
                  </div>
                  
                  {/* Predict Button */}
                  <div className="mb-4">
                    <Button
                      variant="primary"
                      size="lg"
                      onClick={handlePredict}
                      disabled={selectedSymptoms.length === 0 || predicting}
                      className="w-100"
                    >
                      {predicting ? (
                        <>
                          <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            role="status"
                            aria-hidden="true"
                            className="me-2"
                          />
                          Analyzing Symptoms...
                        </>
                      ) : (
                        '🔍 Predict Diseases'
                      )}
                    </Button>
                  </div>
                  
                  {/* Disease Predictions */}
                  <DiseasePredictionCard
                    predictions={predictions}
                    symptoms={selectedSymptoms}
                    loading={predicting}
                    onDiseaseSelect={handleDiseaseSelect}
                  />
                  
                  {/* Confirmed Disease Input */}
                  {predictions.length > 0 && (
                    <div className="mb-3">
                      <label className="form-label fw-bold">Confirmed Diagnosis</label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Enter or select confirmed disease"
                        value={confirmedDisease}
                        onChange={(e) => setConfirmedDisease(e.target.value)}
                        list="disease-suggestions"
                      />
                      <datalist id="disease-suggestions">
                        {predictions.map((pred, idx) => (
                          <option key={idx} value={pred.disease} />
                        ))}
                      </datalist>
                    </div>
                  )}
                  
                  {/* Diagnosis Notes */}
                  {predictions.length > 0 && (
                    <div className="mb-3">
                      <label className="form-label fw-bold">Notes (Optional)</label>
                      <textarea
                        className="form-control"
                        rows="3"
                        placeholder="Add clinical observations, treatment notes, etc."
                        value={diagnosisNotes}
                        onChange={(e) => setDiagnosisNotes(e.target.value)}
                      />
                    </div>
                  )}
                  
                  {/* Create Diagnosis Button */}
                  {selectedPatient && selectedSymptoms.length > 0 && confirmedDisease && (
                    <Button
                      variant="success"
                      size="lg"
                      onClick={handleCreateDiagnosis}
                      disabled={confirmingDiagnosis}
                      className="w-100"
                    >
                      {confirmingDiagnosis ? (
                        <>
                          <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            role="status"
                            aria-hidden="true"
                            className="me-2"
                          />
                          Creating Diagnosis...
                        </>
                      ) : (
                        '✓ Save Diagnosis'
                      )}
                    </Button>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
        
        {/* ==================== PATIENTS TAB ==================== */}
        <Tab eventKey="patients" title="Patients">
          <Row>
            <Col>
              <Card>
                <Card.Header className="d-flex justify-content-between align-items-center">
                  <Card.Title className="mb-0">Patient List</Card.Title>
                  <div style={{ width: '300px' }}>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Search patients..."
                      value={patientSearch}
                      onChange={(e) => setPatientSearch(e.target.value)}
                    />
                  </div>
                </Card.Header>
                <Card.Body>
                  {loadingPatients ? (
                    <div className="text-center py-5">
                      <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </Spinner>
                    </div>
                  ) : patients.length === 0 ? (
                    <Alert variant="info" className="mb-0">
                      No patients found. {patientSearch && 'Try a different search term.'}
                    </Alert>
                  ) : (
                    <div className="table-responsive">
                      <table className="table table-hover">
                        <thead>
                          <tr>
                            <th>Name</th>
                            <th>Phone</th>
                            <th>Blood Type</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {patients.map((patient) => (
                            <tr key={patient.id}>
                              <td>
                                <strong>{patient.first_name} {patient.last_name}</strong>
                              </td>
                              <td>{patient.phone || 'N/A'}</td>
                              <td>{patient.blood_type || 'N/A'}</td>
                              <td>
                                <Button
                                  variant={selectedPatient?.id === patient.id ? 'success' : 'primary'}
                                  size="sm"
                                  onClick={() => {
                                    setSelectedPatient(patient)
                                    setActiveTab('diagnosis')
                                    toast.success(`Selected patient: ${patient.first_name} ${patient.last_name}`)
                                  }}
                                >
                                  {selectedPatient?.id === patient.id ? 'Selected' : 'Select for Diagnosis'}
                                </Button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
        
        {/* ==================== APPOINTMENTS TAB ==================== */}
        <Tab eventKey="appointments" title="Appointments">
          <Row>
            <Col>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">Upcoming Appointments</Card.Title>
                </Card.Header>
                <Card.Body>
                  {loadingAppointments ? (
                    <div className="text-center py-5">
                      <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </Spinner>
                    </div>
                  ) : appointments.length === 0 ? (
                    <Alert variant="info" className="mb-0">
                      No upcoming appointments.
                    </Alert>
                  ) : (
                    <div className="table-responsive">
                      <table className="table table-hover">
                        <thead>
                          <tr>
                            <th>Date & Time</th>
                            <th>Patient</th>
                            <th>Reason</th>
                            <th>Status</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {appointments.map((appointment) => (
                            <tr key={appointment.id}>
                              <td>{formatDate(appointment.appointment_date)}</td>
                              <td>Patient #{appointment.patient_id}</td>
                              <td>{appointment.reason || 'N/A'}</td>
                              <td>
                                <span className={`badge bg-${
                                  appointment.status === 'completed' ? 'success' :
                                  appointment.status === 'cancelled' ? 'danger' : 'warning'
                                }`}>
                                  {appointment.status}
                                </span>
                              </td>
                              <td>
                                <Button variant="outline-primary" size="sm">
                                  View
                                </Button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
      </Tabs>
    </Container>
  )
}

export default DoctorDashboard
