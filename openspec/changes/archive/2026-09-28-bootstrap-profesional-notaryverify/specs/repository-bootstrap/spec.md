# Spec Delta

## Purpose

Define a reproducible, navigable repository baseline for maintaining the
NotaryVerify academic prototype without changing its verification domain.

## ADDED Requirements

### Requirement: Canonical repository orientation
The repository SHALL provide a root README that identifies NotaryVerify as an
academic multicapa identity-verification prototype, states its legal and privacy
limits, and links to the frontend, backend, documentation index, local execution
instructions, and collaboration guidance.

#### Scenario: A contributor starts from the repository root
- **WHEN** a contributor opens the root README
- **THEN** they can identify the purpose, technology boundaries, primary entry
  points, and the documents needed before modifying the prototype

### Requirement: Navigable documentation baseline
The repository SHALL provide a single canonical `documentacion/` index with
linked sections for context, functional requirements, architecture, planning,
quality/operation, and academic source material. Each section SHALL have its own
index and SHALL distinguish current project decisions from material pending
confirmation.

#### Scenario: A contributor needs an architectural or requirement source
- **WHEN** they begin at `documentacion/indice.md`
- **THEN** they can navigate to the applicable section and find the responsible
  source or an explicit pending-decision marker without relying on an external
  or nested repository

### Requirement: Reproducible local configuration
The repository SHALL include a versioned environment-variable example and a
Docker Compose definition that document how to run the existing backend and
frontend locally. The examples SHALL contain no credentials, real personal data,
or biometric samples.

#### Scenario: A developer configures a new checkout
- **WHEN** they follow the documented local setup using the example environment
  file or Docker Compose
- **THEN** they can start the existing prototype components with their documented
  local endpoints and without discovering configuration values from source code

### Requirement: Preservation-aware documentation migration
The repository SHALL inventory the existing `Documentacion/` material before
establishing `documentacion/` as the canonical location. Each retained academic
source SHALL be either linked from or migrated into the canonical index, and no
historical file SHALL be deleted as part of this bootstrap without an explicit
approval recorded in the change execution.

#### Scenario: Existing academic material is incorporated
- **WHEN** the bootstrap is applied
- **THEN** the index records the location and treatment of each existing report
  and identifies the handling of the nested Git repository
