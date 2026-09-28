# role-authorization Specification

## ADDED Requirements

### Requirement: Enforced role matrix

The API SHALL enforce roles independently from the frontend. Administrator-only
operations include identity enrollment and administration, credential
management, and full audit access; verification operations permit Operator or
Administrator.

#### Scenario: Operator requests an administrative resource

- **WHEN** an authenticated Operator requests an administrative or audit route
- **THEN** the API returns HTTP 403 with `AUTHORIZATION_REQUIRED`

### Requirement: Trusted verification responsibility

The API SHALL assign a verification session's responsible actor from the valid
bearer token and SHALL ignore any caller-supplied responsible id.

#### Scenario: Operator starts verification with another id in payload

- **WHEN** an authenticated Operator supplies a different `id_responsable`
- **THEN** the stored session identifies the authenticated Operator
