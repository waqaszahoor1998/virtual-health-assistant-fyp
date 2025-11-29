/**
 * 404 Not Found Page.
 * 
 * Displayed when user navigates to a non-existent route.
 */

import React from 'react'
import { Container, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

function NotFound() {
  const navigate = useNavigate()
  
  return (
    <Container className="text-center py-5">
      <h1>404</h1>
      <p className="lead">Page Not Found</p>
      <p>The page you are looking for does not exist.</p>
      <Button variant="primary" onClick={() => navigate('/')}>
        Go Home
      </Button>
    </Container>
  )
}

export default NotFound

