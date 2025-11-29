/**
 * Navigation Bar Component.
 * 
 * Displays main navigation menu with:
 * - Logo/Brand
 * - Navigation links (role-based)
 * - User menu with logout option
 */

import React from 'react'
import { Navbar as BootstrapNavbar, Nav, Container, Button } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

function Navbar() {
  const navigate = useNavigate()
  const { user, signOut, isAuthenticated } = useAuth()
  
  /**
   * Handle logout button click.
   */
  const handleLogout = async () => {
    try {
      await signOut()
      navigate('/login')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }
  
  return (
    <BootstrapNavbar bg="primary" variant="dark" expand="lg">
      <Container>
        <BootstrapNavbar.Brand as={Link} to="/">
          Virtual Health Assistant
        </BootstrapNavbar.Brand>
        
        <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
        
        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {isAuthenticated && (
              <>
                {user?.role === 'doctor' && (
                  <Nav.Link as={Link} to="/doctor/dashboard">
                    Dashboard
                  </Nav.Link>
                )}
                {user?.role === 'patient' && (
                  <Nav.Link as={Link} to="/patient/dashboard">
                    Dashboard
                  </Nav.Link>
                )}
              </>
            )}
          </Nav>
          
          <Nav>
            {isAuthenticated ? (
              <>
                <Nav.Link disabled>Welcome, {user?.email}</Nav.Link>
                <Button variant="outline-light" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <Nav.Link as={Link} to="/login">
                Login
              </Nav.Link>
            )}
          </Nav>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  )
}

export default Navbar

