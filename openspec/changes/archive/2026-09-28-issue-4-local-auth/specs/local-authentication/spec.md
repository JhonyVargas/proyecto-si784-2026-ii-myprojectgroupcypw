# local-authentication Specification

## Purpose

Provide local development authentication for NotaryVerify's academic Operator
and Administrator roles without exposing sensitive API operations to anonymous
clients.

## ADDED Requirements

### Requirement: Secure local user credentials

The system SHALL store each local user's password only as a salted password
derivation and SHALL never return or log a plaintext password. Development
bootstrap users SHALL be created only from explicit environment configuration.

#### Scenario: Bootstrap a development operator

- **WHEN** complete bootstrap environment values for an operator are supplied
  at startup
- **THEN** the service creates the user with a salted password derivation and
  does not persist the supplied plaintext password

### Requirement: Authenticated session lifecycle

The system SHALL issue an opaque bearer token to a user with valid credentials,
persist only a one-way digest of it, enforce expiry, and permit explicit
revocation through logout.

#### Scenario: Login and logout

- **WHEN** a valid local user logs in and subsequently logs out with its bearer
  token
- **THEN** authentication succeeds before logout and the same token is rejected
  afterward

#### Scenario: Expired or invalid token

- **WHEN** an API dependency receives a missing, invalid, revoked, or expired
  bearer token
- **THEN** it returns HTTP 401 with the stable code `AUTHENTICATION_REQUIRED`
  without indicating which credential component failed

### Requirement: Authenticated actor identity

The system SHALL make the authenticated user's id and role available to API
handlers so later authorization and verification-session features can assign a
responsible actor without trusting a caller-provided identity.

#### Scenario: Resolve current user

- **WHEN** a request has a valid bearer token
- **THEN** the handler receives the corresponding local user identity and role
