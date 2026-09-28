# Spec Delta

## Purpose

Establish explicit collaboration, safety, quality, and traceability expectations
for people and coding agents that contribute to NotaryVerify.

## ADDED Requirements

### Requirement: Contributor and agent preflight
The repository SHALL provide an `AGENTS.md` at the root that requires
contributors and agents to consult the README, applicable canonical
documentation, and active OpenSpec changes before editing. It SHALL identify the
backend, frontend, test, generated-data, and documentation boundaries.

#### Scenario: An agent receives an implementation request
- **WHEN** the agent begins work in the repository
- **THEN** the guidance tells it which project sources to read, which artifacts
  to preserve, and how to determine whether a proposed change needs OpenSpec

### Requirement: Academic-data safety
The collaboration guidance SHALL prohibit committing real client data, real
government credentials, unconsented biometric material, generated SQLite data,
or runtime uploads. It SHALL require the prototype disclaimer to be preserved
in relevant user-facing and documentation changes.

#### Scenario: A contributor prepares a biometric test change
- **WHEN** the change introduces or modifies a test dataset or capture flow
- **THEN** the guidance requires fictitious identities and documented voluntary
  consent before the material can be used

### Requirement: Change quality and traceability
The collaboration guidance SHALL require a focused branch and conventional
commit message, targeted automated tests for changed behavior, and updates to
the applicable documentation or OpenSpec artifacts. It SHALL require an explicit
record when a test cannot run locally.

#### Scenario: A contributor changes backend verification logic
- **WHEN** they prepare the change for review
- **THEN** the change contains the relevant pytest result or a documented reason
  it could not run, and its requirement, design, or operational documentation is
  updated when affected

### Requirement: Controlled persistence changes
The collaboration guidance SHALL require database schema or persisted-data
changes to document compatibility, migration or reset behavior, test impact, and
the handling of development data before implementation. Runtime data and models
shall remain outside version control unless deliberately represented by safe,
synthetic fixtures.

#### Scenario: A contributor changes a SQLAlchemy model
- **WHEN** the change can alter the persisted SQLite schema
- **THEN** its design records how existing local databases are handled and its
  tests cover the expected persistence behavior

### Requirement: Verifiable validation commands
The repository SHALL document the validation commands for the existing backend,
frontend, Docker configuration, and OpenSpec artifacts, with each command's
expected purpose and scope.

#### Scenario: A reviewer validates the bootstrap
- **WHEN** they follow the validation section in the collaboration guidance
- **THEN** they can run the documented checks and determine whether the
  repository baseline is complete
