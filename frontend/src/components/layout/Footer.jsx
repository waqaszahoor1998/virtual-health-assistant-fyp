/**
 * Footer Component.
 * 
 * Displays footer information with:
 * - Copyright notice
 * - Links to important pages
 * - Project information
 */

import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'

function Footer() {
  const currentYear = new Date().getFullYear()
  
  return (
    <footer className="bg-dark text-light py-4 mt-auto">
      <Container>
        <Row>
          <Col md={6}>
            <p className="mb-0">
              &copy; {currentYear} Virtual Health Assistant. All rights reserved.
            </p>
          </Col>
          <Col md={6} className="text-md-end">
            <p className="mb-0 text-muted">
              Final Year Project - Muhammad Rehan Ishaq & Syed Farman Ali
            </p>
          </Col>
        </Row>
      </Container>
    </footer>
  )
}

export default Footer

