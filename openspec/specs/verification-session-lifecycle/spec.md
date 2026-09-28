# verification-session-lifecycle Specification

## Purpose

Define the recoverable, authorized lifecycle and safe history of a verification
session in the local academic prototype.

## Requirements

### Requirement: Recoverable verification session lifecycle

The system SHALL persist the authenticated responsible actor and SHALL expire
an incomplete verification session after ten minutes when it is operated or
queried.

#### Scenario: Query a stale session

- **WHEN** an incomplete session older than ten minutes is queried
- **THEN** it is returned as `EXPIRADA` and cannot accept new factors

### Requirement: Authorized filtered session history

The system SHALL provide Administrators a filterable session history containing
factor outcomes, decision, timestamps, and responsible actor without biometric
samples or paths.

#### Scenario: Filter approved sessions for an identity

- **WHEN** an Administrator filters by identity and approved result
- **THEN** only matching safe session records are returned
