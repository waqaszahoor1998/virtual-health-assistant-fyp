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
import { Container, Row, Col, Card, Tab, Tabs, Button, Alert, Badge, Spinner, Form } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { useAuth } from '../context/AuthContext'
import { patientAPI, diagnosisAPI, prescriptionAPI, appointmentAPI, doctorAPI, consultationAPI } from '../services/api'
import AppointmentBookingModal from '../components/AppointmentBookingModal'
import SymptomSelector from '../components/SymptomSelector'
import DiseasePredictionCard from '../components/DiseasePredictionCard'

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
  const [showBookingModal, setShowBookingModal] = useState(false)

  const commonSymptoms = [
    'fever', 'headache', 'cough', 'nausea', 'fatigue', 'dizziness',
    'chest pain', 'abdominal pain', 'sore throat', 'muscle pain',
    'shortness of breath', 'rash', 'diarrhea', 'vomiting'
  ]
  const [selfSymptoms, setSelfSymptoms] = useState([])
  const [selfPredicting, setSelfPredicting] = useState(false)
  const [selfPredictions, setSelfPredictions] = useState([])

  const [doctors, setDoctors] = useState([])
  const [consultations, setConsultations] = useState([])
  const [loadingConsultations, setLoadingConsultations] = useState(false)
  const [consultSubject, setConsultSubject] = useState('')
  const [consultMessage, setConsultMessage] = useState('')
  const [consultDoctorId, setConsultDoctorId] = useState('')
  const [sendingConsult, setSendingConsult] = useState(false)
  
  /**
   * Load patient profile on component mount.
   */
  useEffect(() => {
    loadPatientProfile()
  }, [user])
  
  /**
   * Load overview data when patient profile is loaded.
   */
  useEffect(() => {
    if (patient) {
      // Load data for overview
      loadPrescriptions()
      loadAppointments()
      loadDiagnosesForOverview()
      loadConsultations()
      loadDoctorsList()
    }
  }, [patient])
  
  /**
   * Load relevant data when tabs change.
   */
  useEffect(() => {
    if (activeTab === 'diagnoses' && patient) {
      loadDiagnoses()
    } else if (activeTab === 'prescriptions' && patient && prescriptions.length === 0) {
      loadPrescriptions()
    } else if (activeTab === 'appointments' && patient && appointments.length === 0) {
      loadAppointments()
    } else if (activeTab === 'consult' && patient && consultations.length === 0) {
      loadConsultations()
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
  const normalizeDiagnosisRow = (row) => {
    let symptoms = row.symptoms
    let predicted = row.predicted_diseases
    try {
      if (typeof symptoms === 'string') symptoms = JSON.parse(symptoms)
    } catch {
      /* keep string */
    }
    try {
      if (typeof predicted === 'string') predicted = JSON.parse(predicted)
    } catch {
      /* keep */
    }
    return { ...row, symptoms, predicted_diseases: predicted }
  }

  const loadDiagnosesForOverview = async () => {
    try {
      const res = await diagnosisAPI.listMine()
      const rows = (res.data.diagnoses || []).map(normalizeDiagnosisRow)
      setDiagnoses(rows)
    } catch {
      setDiagnoses([])
    }
  }

  const loadDiagnoses = async () => {
    setLoadingDiagnoses(true)
    try {
      const res = await diagnosisAPI.listMine()
      const rows = (res.data.diagnoses || []).map(normalizeDiagnosisRow)
      setDiagnoses(rows)
    } catch (error) {
      console.error('Error loading diagnoses:', error)
      toast.error('Failed to load diagnosis history.')
    } finally {
      setLoadingDiagnoses(false)
    }
  }

  const loadDoctorsList = async () => {
    try {
      const res = await doctorAPI.getAll({ per_page: 100 })
      setDoctors(res.data.doctors || [])
    } catch (e) {
      console.error(e)
    }
  }

  const loadConsultations = async () => {
    setLoadingConsultations(true)
    try {
      const res = await consultationAPI.list()
      setConsultations(res.data.consultations || [])
    } catch (e) {
      toast.error('Failed to load messages')
    } finally {
      setLoadingConsultations(false)
    }
  }

  const handleSelfPredict = async () => {
    if (selfSymptoms.length === 0) {
      toast.warning('Select at least one symptom')
      return
    }
    setSelfPredicting(true)
    setSelfPredictions([])
    try {
      const res = await diagnosisAPI.predictSelf(selfSymptoms, 'lightgbm', 5)
      if (res.data.success && res.data.prediction) {
        setSelfPredictions(res.data.prediction.predictions || [])
        toast.success('Possible conditions generated (informational only).')
      }
    } catch (e) {
      toast.error(e.response?.data?.error || 'Prediction failed')
    } finally {
      setSelfPredicting(false)
    }
  }

  const sendConsultation = async (e) => {
    e.preventDefault()
    if (!consultSubject.trim() || !consultMessage.trim()) {
      toast.error('Subject and message are required')
      return
    }
    setSendingConsult(true)
    try {
      await consultationAPI.create({
        subject: consultSubject.trim(),
        message: consultMessage.trim(),
        doctor_id: consultDoctorId ? parseInt(consultDoctorId, 10) : undefined,
        symptoms: selfSymptoms.length ? selfSymptoms : undefined,
      })
      toast.success('Message sent to your care team')
      setConsultSubject('')
      setConsultMessage('')
      loadConsultations()
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to send')
    } finally {
      setSendingConsult(false)
    }
  }

  const cancelAppointment = async (appointment) => {
    if (!window.confirm('Cancel this appointment?')) return
    try {
      await appointmentAPI.update(appointment.id, { status: 'cancelled' })
      toast.success('Appointment cancelled')
      loadAppointments()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Could not cancel')
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
                    <Button variant="warning" onClick={() => setActiveTab('symptom_check')}>
                      🤒 Symptom check (AI)
                    </Button>
                    <Button variant="secondary" onClick={() => setActiveTab('consult')}>
                      ✉️ Message a doctor
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
                  <Button variant="primary" size="sm" onClick={() => setShowBookingModal(true)}>
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
                              <td>
                                {doctors.find((d) => d.id === appointment.doctor_id)
                                  ? `Dr. ${doctors.find((d) => d.id === appointment.doctor_id).first_name} ${doctors.find((d) => d.id === appointment.doctor_id).last_name}`
                                  : `Doctor #${appointment.doctor_id}`}
                              </td>
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
                                  <Button variant="outline-danger" size="sm" onClick={() => cancelAppointment(appointment)}>
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
                                {Array.isArray(diagnosis.symptoms) && diagnosis.symptoms.length > 0 && (
                                  <p className="small mb-1">
                                    <strong>Symptoms:</strong> {diagnosis.symptoms.join(', ')}
                                  </p>
                                )}
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

        <Tab eventKey="symptom_check" title="Symptom check">
          <Alert variant="warning">
            This is an informational tool only. It does not replace a clinician. Share results with your doctor using &quot;Message a doctor&quot;.
          </Alert>
          <Card className="mb-3">
            <Card.Header><Card.Title className="mb-0">Your symptoms</Card.Title></Card.Header>
            <Card.Body>
              <SymptomSelector
                selectedSymptoms={selfSymptoms}
                onSymptomsChange={setSelfSymptoms}
                availableSymptoms={commonSymptoms}
                maxSymptoms={15}
              />
              <Button className="mt-3" onClick={handleSelfPredict} disabled={selfPredicting || selfSymptoms.length === 0}>
                {selfPredicting ? 'Analyzing…' : 'What might this be?'}
              </Button>
            </Card.Body>
          </Card>
          <DiseasePredictionCard
            predictions={selfPredictions}
            symptoms={selfSymptoms}
            loading={selfPredicting}
          />
        </Tab>

        <Tab eventKey="consult" title="Doctor messages">
          <Row>
            <Col md={5}>
              <Card className="mb-3">
                <Card.Header><Card.Title className="mb-0">Ask a doctor</Card.Title></Card.Header>
                <Card.Body>
                  <Form onSubmit={sendConsultation}>
                    <Form.Group className="mb-2">
                      <Form.Label>Doctor (optional)</Form.Label>
                      <Form.Select value={consultDoctorId} onChange={(e) => setConsultDoctorId(e.target.value)}>
                        <option value="">Any available doctor</option>
                        {doctors.map((d) => (
                          <option key={d.id} value={d.id}>
                            Dr. {d.first_name} {d.last_name}{d.specialization ? ` — ${d.specialization}` : ''}
                          </option>
                        ))}
                      </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Subject</Form.Label>
                      <Form.Control value={consultSubject} onChange={(e) => setConsultSubject(e.target.value)} required />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Message</Form.Label>
                      <Form.Control as="textarea" rows={4} value={consultMessage} onChange={(e) => setConsultMessage(e.target.value)} required />
                    </Form.Group>
                    <Button type="submit" disabled={sendingConsult}>{sendingConsult ? 'Sending…' : 'Send'}</Button>
                  </Form>
                </Card.Body>
              </Card>
            </Col>
            <Col md={7}>
              <Card>
                <Card.Header><Card.Title className="mb-0">Inbox</Card.Title></Card.Header>
                <Card.Body>
                  {loadingConsultations ? (
                    <div className="text-center py-4"><Spinner animation="border" /></div>
                  ) : consultations.length === 0 ? (
                    <Alert variant="info" className="mb-0">No messages yet.</Alert>
                  ) : (
                    consultations.map((c) => (
                      <Card key={c.id} className="mb-2">
                        <Card.Body>
                          <div className="d-flex justify-content-between">
                            <strong>{c.subject}</strong>
                            <Badge bg="secondary">{c.status}</Badge>
                          </div>
                          <p className="mb-1 mt-2">{c.message}</p>
                          {c.doctor_response && (
                            <Alert variant="success" className="mb-0 py-2">
                              <strong>Doctor:</strong> {c.doctor_response}
                            </Alert>
                          )}
                        </Card.Body>
                      </Card>
                    ))
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
      </Tabs>
      
      {/* Appointment Booking Modal */}
      <AppointmentBookingModal
        show={showBookingModal}
        onHide={() => setShowBookingModal(false)}
        onSuccess={(appointment) => {
          // Reload appointments after successful booking
          loadAppointments()
          setShowBookingModal(false)
        }}
      />
    </Container>
  )
}

export default PatientDashboard
