/**
 * Symptom Selector Component.
 * 
 * Allows users (doctors) to select symptoms from a list or type custom symptoms.
 * Used in the diagnosis interface.
 */

import React, { useState, useEffect } from 'react'
import { Form, InputGroup, Button, ListGroup, Badge, Alert } from 'react-bootstrap'
// Icons using Unicode symbols (no external dependency needed)
// Alternative: Install react-bootstrap-icons or use Font Awesome

/**
 * SymptomSelector Component
 * 
 * @param {Array} selectedSymptoms - Currently selected symptoms
 * @param {Function} onSymptomsChange - Callback when symptoms change
 * @param {Array} availableSymptoms - Optional: predefined list of symptoms to choose from
 * @param {number} maxSymptoms - Maximum number of symptoms allowed (default: 10)
 */
function SymptomSelector({
    selectedSymptoms = [],
    onSymptomsChange,
    availableSymptoms = [],
    maxSymptoms = 10
}) {
    // State for search input
    const [searchTerm, setSearchTerm] = useState('')
    
    // State for custom symptom input
    const [customSymptom, setCustomSymptom] = useState('')
    
    // Filtered available symptoms based on search
    const filteredSymptoms = availableSymptoms.filter(symptom =>
        symptom.toLowerCase().includes(searchTerm.toLowerCase()) &&
        !selectedSymptoms.includes(symptom)
    )
    
    /**
     * Handle adding a symptom from the list.
     */
    const handleAddSymptom = (symptom) => {
        if (selectedSymptoms.length >= maxSymptoms) {
            return
        }
        
        if (!selectedSymptoms.includes(symptom)) {
            const newSymptoms = [...selectedSymptoms, symptom]
            onSymptomsChange(newSymptoms)
            setSearchTerm('') // Clear search after selection
        }
    }
    
    /**
     * Handle adding a custom symptom.
     */
    const handleAddCustomSymptom = () => {
        if (!customSymptom.trim()) {
            return
        }
        
        const trimmedSymptom = customSymptom.trim().toLowerCase()
        
        // Check if already added
        if (selectedSymptoms.includes(trimmedSymptom)) {
            return
        }
        
        // Check max limit
        if (selectedSymptoms.length >= maxSymptoms) {
            return
        }
        
        // Add custom symptom
        const newSymptoms = [...selectedSymptoms, trimmedSymptom]
        onSymptomsChange(newSymptoms)
        setCustomSymptom('') // Clear input
    }
    
    /**
     * Handle removing a symptom.
     */
    const handleRemoveSymptom = (symptomToRemove) => {
        const newSymptoms = selectedSymptoms.filter(s => s !== symptomToRemove)
        onSymptomsChange(newSymptoms)
    }
    
    /**
     * Handle Enter key press in custom symptom input.
     */
    const handleCustomSymptomKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            handleAddCustomSymptom()
        }
    }
    
    return (
        <div className="symptom-selector">
            {/* Selected Symptoms Display */}
            <div className="mb-3">
                <label className="form-label">
                    Selected Symptoms ({selectedSymptoms.length}/{maxSymptoms})
                </label>
                
                {selectedSymptoms.length === 0 ? (
                    <Alert variant="info" className="mb-0">
                        No symptoms selected. Add symptoms from the list below or type custom symptoms.
                    </Alert>
                ) : (
                    <div className="d-flex flex-wrap gap-2">
                        {selectedSymptoms.map((symptom, index) => (
                            <Badge
                                key={index}
                                bg="primary"
                                className="d-flex align-items-center gap-2"
                                style={{ fontSize: '0.9rem', padding: '0.5rem' }}
                            >
                                <span>{symptom}</span>
                                <Button
                                    variant="link"
                                    size="sm"
                                    className="p-0 text-white"
                                    onClick={() => handleRemoveSymptom(symptom)}
                                    style={{ 
                                        lineHeight: 1, 
                                        textDecoration: 'none',
                                        minWidth: 'auto'
                                    }}
                                >
                                    ✕
                                </Button>
                            </Badge>
                        ))}
                    </div>
                )}
            </div>
            
            {/* Custom Symptom Input */}
            <div className="mb-3">
                <label className="form-label">Add Custom Symptom</label>
                <InputGroup>
                    <Form.Control
                        type="text"
                        placeholder="Type a symptom and press Enter or click Add"
                        value={customSymptom}
                        onChange={(e) => setCustomSymptom(e.target.value)}
                        onKeyPress={handleCustomSymptomKeyPress}
                        disabled={selectedSymptoms.length >= maxSymptoms}
                    />
                    <Button
                        variant="success"
                        onClick={handleAddCustomSymptom}
                        disabled={
                            !customSymptom.trim() || 
                            selectedSymptoms.length >= maxSymptoms ||
                            selectedSymptoms.includes(customSymptom.trim().toLowerCase())
                        }
                    >
                        +
                        Add
                    </Button>
                </InputGroup>
            </div>
            
            {/* Available Symptoms Search */}
            {availableSymptoms.length > 0 && (
                <div className="mb-3">
                    <label className="form-label">Search Available Symptoms</label>
                    <InputGroup className="mb-2">
                        <InputGroup.Text>
                            🔍
                        </InputGroup.Text>
                        <Form.Control
                            type="text"
                            placeholder="Search symptoms..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </InputGroup>
                    
                    {/* Filtered Symptoms List */}
                    {searchTerm && filteredSymptoms.length > 0 && (
                        <ListGroup style={{ maxHeight: '200px', overflowY: 'auto' }}>
                            {filteredSymptoms.slice(0, 10).map((symptom, index) => (
                                <ListGroup.Item
                                    key={index}
                                    action
                                    onClick={() => handleAddSymptom(symptom)}
                                    className="d-flex justify-content-between align-items-center"
                                >
                                    <span>{symptom}</span>
                                    <Button
                                        variant="outline-primary"
                                        size="sm"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            handleAddSymptom(symptom)
                                        }}
                                    >
                                        +
                                    </Button>
                                </ListGroup.Item>
                            ))}
                        </ListGroup>
                    )}
                    
                    {searchTerm && filteredSymptoms.length === 0 && (
                        <Alert variant="warning" className="mb-0">
                            No matching symptoms found. You can add it as a custom symptom above.
                        </Alert>
                    )}
                </div>
            )}
            
            {/* Warning if max symptoms reached */}
            {selectedSymptoms.length >= maxSymptoms && (
                <Alert variant="warning" className="mt-2">
                    Maximum {maxSymptoms} symptoms reached. Remove a symptom to add another.
                </Alert>
            )}
        </div>
    )
}

export default SymptomSelector

