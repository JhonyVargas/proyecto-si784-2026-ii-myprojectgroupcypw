# authorized-biometric-reference-change Specification

## Purpose

Define consent-aware, role-separated, and safely retained changes to a local
synthetic biometric reference.

## Requirements

### Requirement: Requested and authorized reference changes

The system SHALL require valid biometric consent to request a synthetic facial
reference change and SHALL require an Administrator to approve or reject it.
An Operator SHALL not decide a request.

#### Scenario: Operator requests a replacement

- **WHEN** an Operator with valid consent submits a new local reference and reason
- **THEN** a pending request is created and the Operator cannot approve it

### Requirement: Safe retention and auditable decision

The system SHALL replace the active local reference and remove the prior file
upon approval, or remove the pending file upon rejection. Audit events SHALL
include actor, reason, date, and outcome but no image or filesystem path.

#### Scenario: Administrator rejects a pending reference

- **WHEN** an Administrator rejects a pending request with a reason
- **THEN** the pending image is deleted and an auditable rejection is recorded
