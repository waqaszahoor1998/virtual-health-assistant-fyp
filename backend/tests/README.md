# Backend Tests

## Overview

This directory contains tests for the backend API. Tests are organized by module.

## Structure

```
tests/
├── __init__.py
├── test_models/          # Database model tests
├── test_api/            # API endpoint tests
└── test_utils/          # Utility function tests
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models/test_user.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v
```

## Test Setup

Tests use the `testing` configuration from `config.py` which uses an in-memory SQLite database.

## Status

Tests are not yet implemented. This directory is ready for test development.

