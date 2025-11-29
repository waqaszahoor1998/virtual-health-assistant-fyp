/**
 * Doctor Dashboard Page.
 * 
 * Main dashboard for doctors showing:
 * - Patient list
 * - Upcoming appointments
 * - Quick actions (diagnosis, prescriptions)
 */

import React from 'react'
import { Container, Row, Col, Card } from 'react-bootstrap'

function DoctorDashboard() {
  return (
    <Container className="py-4">
      <h1 className="mb-4">Doctor Dashboard</h1>
      
      <Row>
        <Col md={4}>
          <Card className="mb-3">
            <Card.Body>
              <Card.Title>Quick Actions</Card.Title>
              <p>Create diagnosis, view patients, manage appointments</p>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={8}>
          <Card>
            <Card.Body>
              <Card.Title>Upcoming Appointments</Card.Title>
              <p>Appointments list will appear here</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default DoctorDashboard

