/**
 * Disease Prediction Card Component.
 * 
 * Displays ML model predictions for diseases with confidence scores.
 * Shows top predicted diseases with visual confidence indicators.
 */

import React from 'react'
import { Card, ListGroup, Badge, ProgressBar, Alert } from 'react-bootstrap'

/**
 * DiseasePredictionCard Component
 * 
 * @param {Array} predictions - Array of prediction objects with disease and confidence
 * @param {string} modelUsed - Name of the ML model used (e.g., "XGBoost")
 * @param {Array} symptoms - List of symptoms that were used for prediction
 * @param {boolean} loading - Loading state
 * @param {Function} onDiseaseSelect - Optional callback when disease is selected
 */
function DiseasePredictionCard({
    predictions = [],
    modelUsed = 'XGBoost',
    symptoms = [],
    loading = false,
    onDiseaseSelect = null
}) {
    /**
     * Get variant color based on confidence score.
     */
    const getConfidenceColor = (confidence) => {
        if (confidence >= 0.7) return 'success'
        if (confidence >= 0.4) return 'warning'
        return 'danger'
    }
    
    /**
     * Format confidence as percentage.
     */
    const formatConfidence = (confidence) => {
        return `${(confidence * 100).toFixed(1)}%`
    }
    
    if (loading) {
        return (
            <Card className="mb-3">
                <Card.Body>
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </div>
                        <p className="mt-2 mb-0">Analyzing symptoms...</p>
                    </div>
                </Card.Body>
            </Card>
        )
    }
    
    if (predictions.length === 0) {
        return (
            <Card className="mb-3">
                <Card.Body>
                    <Alert variant="info" className="mb-0">
                        No predictions available. Select symptoms and click "Predict" to see disease predictions.
                    </Alert>
                </Card.Body>
            </Card>
        )
    }
    
    return (
        <Card className="mb-3">
            <Card.Header className="d-flex justify-content-between align-items-center">
                <Card.Title className="mb-0">Disease Predictions</Card.Title>
                <Badge bg="secondary">{modelUsed}</Badge>
            </Card.Header>
            <Card.Body>
                {/* Symptoms Used */}
                {symptoms.length > 0 && (
                    <div className="mb-3">
                        <small className="text-muted">Symptoms analyzed:</small>
                        <div className="d-flex flex-wrap gap-1 mt-1">
                            {symptoms.map((symptom, idx) => (
                                <Badge key={idx} bg="info" text="dark">
                                    {symptom}
                                </Badge>
                            ))}
                        </div>
                    </div>
                )}
                
                {/* Predictions List */}
                <ListGroup variant="flush">
                    {predictions.map((prediction, index) => (
                        <ListGroup.Item
                            key={index}
                            action={onDiseaseSelect !== null}
                            onClick={() => onDiseaseSelect && onDiseaseSelect(prediction.disease)}
                            className="px-0"
                        >
                            <div className="d-flex justify-content-between align-items-start mb-2">
                                <div className="flex-grow-1">
                                    <h6 className="mb-1">{prediction.disease}</h6>
                                    <div className="d-flex align-items-center gap-2">
                                        <ProgressBar
                                            now={prediction.confidence * 100}
                                            variant={getConfidenceColor(prediction.confidence)}
                                            style={{ width: '150px', height: '8px' }}
                                        />
                                        <small className="text-muted">
                                            {formatConfidence(prediction.confidence)}
                                        </small>
                                    </div>
                                </div>
                                {index === 0 && prediction.confidence > 0.5 && (
                                    <Badge bg={getConfidenceColor(prediction.confidence)}>
                                        Top Match
                                    </Badge>
                                )}
                            </div>
                        </ListGroup.Item>
                    ))}
                </ListGroup>
                
                {/* Disclaimer */}
                <Alert variant="warning" className="mt-3 mb-0" style={{ fontSize: '0.875rem' }}>
                    <strong>⚠️ Medical Disclaimer:</strong> This prediction is for informational 
                    purposes only and should not replace professional medical diagnosis. 
                    Always consult with a qualified healthcare provider.
                </Alert>
            </Card.Body>
        </Card>
    )
}

export default DiseasePredictionCard

