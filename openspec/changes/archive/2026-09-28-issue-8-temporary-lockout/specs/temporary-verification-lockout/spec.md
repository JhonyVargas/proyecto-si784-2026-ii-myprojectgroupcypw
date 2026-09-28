# temporary-verification-lockout Specification

## ADDED Requirements

### Requirement: Traceable temporary lockout

The system SHALL create an auditable temporary alert after three consecutive
failed sessions and SHALL reject new verification attempts during its 15-minute
validity without permanently disabling the identity.

#### Scenario: Third consecutive rejection

- **WHEN** an identity accumulates three consecutive rejected sessions
- **THEN** an alert records the count and expiry, and subsequent attempts return
  `IDENTITY_TEMPORARILY_LOCKED`

### Requirement: Controlled recovery

The system SHALL resolve an expired alert automatically and SHALL allow an
Administrator to reactivate an active alert with an audit event.

#### Scenario: Lock expiry

- **WHEN** the alert's expiration time has passed
- **THEN** the identity can resume the defined flow without permanent state change
