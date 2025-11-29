/**
 * Patient Dashboard Page.
 * 
 * Main dashboard for patients showing:
 * - Medical history and diagnoses
 * - Active and past prescriptions
 * - Upcoming and past appointments
 * - Profile information
 * - Quick actions (request appointment, view prescriptions)
 */

import React, { useState, useEffect } from 'react'
import { Container, Row, Col, Card, Tab, Tabs, Button, Alert, Badge, Spinner } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { useAuth } from '../context/AuthContext'
import { patientAPI, diagnosisAPI, prescriptionAPI, appointmentAPI } from '../services/api'

/**
 * Main Patient Dashboard component.
 */
function PatientDashboard() {
  // Authentication context
  const { user } = useAuth()
  
  // Active tab state
  const [activeTab, setActiveTab] = useState('overview')
  
  // ==================== STATE VARIABLES ====================
  const [patient, setPatient] = useState(null)
  const [loadingPatient, setLoadingPatient] = useState(true)
  const [diagnoses, setDiagnoses] = useState([])
  const [loadingDiagnoses, setLoadingDiagnoses] = useState(false)
  const [prescriptions, setPrescriptions] = useState([])
  const [loadingPrescriptions, setLoadingPrescriptions] = useState(false)
  const [appointments, setAppointments] = useState([])
  const [loadingAppointments, setLoadingAppointments] = useState(false)
  
  /**
   * Load patient profile on component mount.
   */
  useEffect(() => {
    loadPatientProfile()
  }, [user])
  
  /**
   * Load relevant data when tabs change.
   */
  useEffect(() => {
    if (activeTab === 'diagnoses' && patient) {
      loadDiagnoses()
    } else if (activeTab === 'prescriptions' && patient) {
      loadPrescriptions()
    } else if (activeTab === 'appointments' && patient) {
      loadAppointments()
    }
  }, [activeTab, patient])
  
  /**
   * Load patient profile information.
   */
  const loadPatientProfile = async () => {
    setLoadingPatient(true)
    try {
      const response = await patientAPI.getAll()
      // Patients get only their own profile
      if (response.data.patients && response.data.patients.length > 0) {
        setPatient(response.data.patients[0])
      }
    } catch (error) {
      console.error('Error loading patient profile:', error)
      toast.error('Failed to load profile. Please try again.')
    } finally {
      setLoadingPatient(false)
    }
  }
  
  /**
   * Load patient diagnoses (if API endpoint exists).
   * Note: This would need a backend endpoint like GET /diagnosis/patient/:patient_id
   */
  const loadDiagnoses = async () => {
    setLoadingDiagnoses(true)
    try {
      // TODO: Implement endpoint to get patient diagnoses
      // For now, show placeholder
      setDiagnoses([])
      toast.info('Diagnosis history will be available soon')
    } catch (error) {
      console.error('Error loading diagnoses:', error)
      toast.error('Failed to load diagnosis history.')
    } finally {
      setLoadingDiagnoses(false)
    }
  }
  
  /**
   * Load patient prescriptions.
   */
  const loadPrescriptions = async () => {
    if (!patient) return
    
    setLoadingPrescriptions(true)
    try {
      const response = await prescriptionAPI.getByPatient(patient.id)
      setPrescriptions(response.data.prescriptions || [])
    } catch (error) {
      console.error('Error loading prescriptions:', error)
      toast.error('Failed to load prescriptions. Please try again.')
    } finally {
      setLoadingPrescriptions(false)
    }
  }
  
  /**
   * Load patient appointments.
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
  
  /**
   * Format date (date only, no time).
   */
  const formatDateOnly = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
  
  if (loadingPatient) {
    return (
      <Container className="py-5">
        <div className="text-center">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </div>
      </Container>
    )
  }
  
  return (
    <Container fluid className="py-4">
      {/* Dashboard Header */}
      <Row className="mb-4">
        <Col>
          <h1 className="mb-1">Patient Dashboard</h1>
          <p className="text-muted">
            Welcome back, {patient ? `${patient.first_name} ${patient.last_name}` : user?.email || 'Patient'}
          </p>
        </Col>
      </Row>
      
      {/* Overview Cards */}
      {activeTab === 'overview' && (
        <Row className="mb-4">
          <Col md={4}>
            <Card className="text-center mb-3">
              <Card.Body>
                <h3>{appointments.filter(a => a.status === 'scheduled').length}</h3>
                <p className="text-muted mb-0">Upcoming Appointments</p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4}>
            <Card className="text-center mb-3">
              <Card.Body>
                <h3>{prescriptions.length}</h3>
                <p className="text-muted mb-0">Active Prescriptions</p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4}>
            <Card className="text-center mb-3">
              <Card.Body>
                <h3>{diagnoses.length}</h3>
                <p className="text-muted mb-0">Recent Diagnoses</p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
      
      {/* Main Content Tabs */}
      <Tabs
        activeKey={activeTab}
        onSelect={(k) => setActiveTab(k)}
        className="mb-4"
      >
        {/* ==================== OVERVIEW TAB ==================== */}
        <Tab eventKey="overview" title="Overview">
          <Row>
            <Col md={6}>
              <Card className="mb-4">
                <Card.Header>
                  <Card.Title className="mb-0">Profile Information</Card.Title>
                </Card.Header>
                <Card.Body>
                  {patient ? (
                    <div>
                      <p><strong>Name:</strong> {patient.first_name} {patient.last_name}</p>
                      {patient.phone && <p><strong>Phone:</strong> {patient.phone}</p>}
                      {patient.blood_type && <p><strong>Blood Type:</strong> {patient.blood_type}</p>}
                      {patient.allergies && (
                        <div>
                          <strong>Allergies:</strong>
                          <div className="mt-1">
                            {patient.allergies.split(',').map((allergy, idx) => (
                              <Badge key={idx} bg="warning" className="me-1">
                                {allergy.trim()}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <Alert variant="info">Complete your profile to see information here.</Alert>
                  )}
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={6}>
              <Card className="mb-4">
                <Card.Header>
                  <Card.Title className="mb-0">Quick Actions</Card.Title>
                </Card.Header>
                <Card.Body>
                  <div className="d-grid gap-2">
                    <Button variant="primary" onClick={() => setActiveTab('appointments')}>
                      📅 View Appointments
                    </Button>
                    <Button variant="success" onClick={() => setActiveTab('prescriptions')}>
                      💊 View Prescriptions
                    </Button>
                    <Button variant="info" onClick={() => setActiveTab('diagnoses')}>
                      📋 View Medical History
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
        
        {/* ==================== PRESCRIPTIONS TAB ==================== */}
        <Tab eventKey="prescriptions" title="Prescriptions">
          <Row>
            <Col>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">My Prescriptions</Card.Title>
                </Card.Header>
                <Card.Body>
                  {loadingPrescriptions ? (
                    <div className="text-center py-5">
                      <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </Spinner>
                    </div>
                  ) : prescriptions.length === 0 ? (
                    <Alert variant="info" className="mb-0">
                      No prescriptions found.
                    </Alert>
                  ) : (
                    <div className="table-responsive">
                      <table className="table table-hover">
                        <thead>
                          <tr>
                            <th>Date</th>
                            <th>Drug Name</th>
                            <th>Dosage</th>
                            <th>Frequency</th>
                            <th>Duration</th>
                            <th>Instructions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {prescriptions.map((prescription) => (
                            <tr key={prescription.id}>
                              <td>{formatDateOnly(prescription.created_at)}</td>
                              <td><strong>{prescription.drug_name}</strong></td>
                              <td>{prescription.dosage || 'N/A'}</td>
                              <td>{prescription.frequency || 'N/A'}</td>
                              <td>{prescription.duration || 'N/A'}</td>
                              <td>{prescription.instructions || 'N/A'}</td>
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
                <Card.Header className="d-flex justify-content-between align-items-center">
                  <Card.Title className="mb-0">My Appointments</Card.Title>
                  <Button variant="primary" size="sm">
                    + Request Appointment
                  </Button>
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
                      No appointments scheduled. Click "Request Appointment" to book one.
                    </Alert>
                  ) : (
                    <div className="table-responsive">
                      <table className="table table-hover">
                        <thead>
                          <tr>
                            <th>Date & Time</th>
                            <th>Doctor</th>
                            <th>Reason</th>
                            <th>Status</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {appointments.map((appointment) => (
                            <tr key={appointment.id}>
                              <td>{formatDate(appointment.appointment_date)}</td>
                              <td>Doctor #{appointment.doctor_id}</td>
                              <td>{appointment.reason || 'N/A'}</td>
                              <td>
                                <Badge bg={
                                  appointment.status === 'completed' ? 'success' :
                                  appointment.status === 'cancelled' ? 'danger' : 'warning'
                                }>
                                  {appointment.status}
                                </Badge>
                              </td>
                              <td>
                                <Button variant="outline-primary" size="sm" className="me-2">
                                  View
                                </Button>
                                {appointment.status === 'scheduled' && (
                                  <Button variant="outline-danger" size="sm">
                                    Cancel
                                  </Button>
                                )}
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
        
        {/* ==================== MEDICAL HISTORY TAB ==================== */}
        <Tab eventKey="diagnoses" title="Medical History">
          <Row>
            <Col>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">Diagnosis History</Card.Title>
                </Card.Header>
                <Card.Body>
                  {loadingDiagnoses ? (
                    <div className="text-center py-5">
                      <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </Spinner>
                    </div>
                  ) : diagnoses.length === 0 ? (
                    <Alert variant="info" className="mb-0">
                      No diagnosis history available yet.
                    </Alert>
                  ) : (
                    <div>
                      {diagnoses.map((diagnosis) => (
                        <Card key={diagnosis.id} className="mb-3">
                          <Card.Body>
                            <div className="d-flex justify-content-between">
                              <div>
                                <h5>{diagnosis.confirmed_disease || 'Diagnosis'}</h5>
                                <p className="text-muted mb-2">
                                  {formatDate(diagnosis.created_at)}
                                </p>
                                {diagnosis.notes && (
                                  <p className="mb-0">{diagnosis.notes}</p>
                                )}
                              </div>
                            </div>
                          </Card.Body>
                        </Card>
                      ))}
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

export default PatientDashboard
