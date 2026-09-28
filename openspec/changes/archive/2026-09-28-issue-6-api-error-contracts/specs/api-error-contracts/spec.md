# api-error-contracts Specification

## ADDED Requirements

### Requirement: Stable domain rejection contract

The API SHALL return domain rejections as an HTTP status and an object with a
stable `detail.code`, without requiring clients to parse internal messages.

#### Scenario: Missing credential

- **WHEN** an authenticated client requests an unknown credential
- **THEN** the API returns HTTP 404 and `detail.code` `CREDENTIAL_NOT_FOUND`
