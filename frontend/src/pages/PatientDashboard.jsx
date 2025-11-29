/**
 * Patient Dashboard Page.
 * 
 * Main dashboard for patients showing:
 * - Medical history
 * - Upcoming appointments
 * - Prescriptions
 * - Quick actions
 */

import React from 'react'
import { Container, Row, Col, Card } from 'react-bootstrap'

function PatientDashboard() {
  return (
    <Container className="py-4">
      <h1 className="mb-4">Patient Dashboard</h1>
      
      <Row>
        <Col md={6}>
          <Card className="mb-3">
            <Card.Body>
              <Card.Title>Upcoming Appointments</Card.Title>
              <p>Your appointments will appear here</p>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card className="mb-3">
            <Card.Body>
              <Card.Title>Recent Prescriptions</Card.Title>
              <p>Your prescriptions will appear here</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default PatientDashboard

