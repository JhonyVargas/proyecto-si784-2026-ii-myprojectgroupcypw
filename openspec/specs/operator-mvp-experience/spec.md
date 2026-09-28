# operator-mvp-experience Specification

## Purpose

Define the authenticated, safe, and recoverable four-step user experience for
the local NotaryVerify operator station.

## Requirements

### Requirement: Authenticated four-step operator flow

The station SHALL require an authenticated Operator or Administrator before it
starts verification and SHALL guide the user through credential, face, liveness,
and result without exposing administration to an Operator.

#### Scenario: Anonymous station load

- **WHEN** the station has no valid local session
- **THEN** it explains that Operator login is required and disables flow start

### Requirement: Recoverable operator errors

The station SHALL display actionable safe messages for expired sessions,
temporary lockout, denied authorization, camera failure, and unavailable API.

#### Scenario: Expired verification session

- **WHEN** the API returns `SESSION_NOT_ACTIVE`
- **THEN** the operator sees an expiration message and can start a new flow
