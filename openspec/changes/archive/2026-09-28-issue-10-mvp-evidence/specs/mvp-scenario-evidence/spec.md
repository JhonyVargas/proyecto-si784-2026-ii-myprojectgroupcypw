# mvp-scenario-evidence Specification

## ADDED Requirements

### Requirement: Reproducible critical MVP scenarios

The repository SHALL automate the approved flow, non-matching face, failed
liveness, and unknown credential scenarios with synthetic fixtures that do not
require a camera, an external image, or model download.

#### Scenario: Execute MVP evidence suite offline

- **WHEN** the test suite executes without biometric network resources
- **THEN** all four critical M1 scenarios produce their expected persisted result

### Requirement: Clear evidence scope

The quality documentation SHALL distinguish deterministic technical tests from
manual demonstration and future experimental biometric evaluation.

#### Scenario: Reviewer reads M1 quality evidence

- **WHEN** a reviewer opens the test strategy
- **THEN** they can identify the four automated scenarios and their limitations
