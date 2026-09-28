# simulated-rfid-credential Specification

## ADDED Requirements

### Requirement: Canonical simulated RFID read

The system SHALL support a simulated RFID adapter that accepts an uppercase,
separator-free hexadecimal UID and retrieves only its associated RFID
credential without requiring physical hardware.

#### Scenario: Read a simulated UID

- **WHEN** a canonical UID such as `04A1B2C3` is read
- **THEN** the adapter returns the associated RFID credential under the same
  credential contract used by QR

### Requirement: RFID state parity and no standalone approval

The simulated RFID reader SHALL preserve missing and revoked credential
behavior and SHALL not approve a verification session without facial and
liveness factors.

#### Scenario: Read a revoked simulated RFID credential

- **WHEN** a revoked RFID UID is read and used to start verification
- **THEN** it remains revoked and the session is rejected
