# Design

## Context

The repository contains a partially implemented FastAPI, SQLite and static
frontend prototype with academic requirements in the preserved FD03 SRS. Before
this change, GitHub had labels but no issues or milestones, while the canonical
roadmap described only broad phases. GitHub Projects cannot be inspected or
configured with the current token because it lacks the `read:project` scope.

## Goals / Non-Goals

**Goals:**

- Make GitHub Issues and Milestones the execution state for implementation.
- Use actual SRS identifiers, source modules, tests, dependencies, and
  phase/MVP classification in a canonical local planning mirror.
- Keep the plan valid when GitHub Projects permissions remain unavailable.

**Non-Goals:**

- Change product behavior, endpoints, schemas, algorithms, or the existing
  verification flow.
- Treat an issue title or milestone as evidence that a requirement is complete.
- Create a second product backlog outside GitHub.

## Decisions

### GitHub Issues plus Milestones are the master execution model

Each issue is a pull-request-sized unit with a standard body, labels and a
milestone. Eight milestones represent demonstrable outcomes from MVP through
final delivery. This avoids a GitHub Project dependency while preserving an
ordered, auditable path. A Project can be added later only after access is
available and without duplicating these fields.

### Documentation mirrors identifiers, not bodies

Canonical planning files summarize the roadmap, dependency graph, requirements
coverage, implementation status, and next ready issue. They link issue numbers
instead of copying full issue bodies, so GitHub remains the editable work queue
and documentation remains the academic traceability source.

### Implementation and evaluation stay separate

Issues that construct or harden a feature use MVP or V1 phases. Protocols that
measure biometric and liveness outcomes use the experimental phase and require
consent, synthetic/fictitious identities where applicable, aggregate evidence,
and documented limitations.

## Risks / Trade-offs

- [GitHub Project permissions unavailable] → Use Issues plus Milestones now;
  record the limitation and revisit only after scopes are granted.
- [Prototype claims outrun evidence] → Mark current features as implemented,
  partial, or unstarted and reserve completion for issue acceptance evidence.
- [Plan becomes stale] → Require each implementation pull request to update its
  issue, linked documentation, and traceability row.
- [Biometric evaluation introduces sensitive material] → Require voluntary
  consent, no real client data, and aggregate reporting before experiments.

## Migration Plan

1. Create labels, milestones and executable issues from the audited code/SRS.
2. Publish canonical roadmap, backlog, phases and traceability linked to the
   GitHub identifiers.
3. Validate links, issue metadata, OpenSpec artifacts and documentation before
   committing the planning branch.
4. Open a pull request; rollback consists of reverting the documentation and
   closing or relabeling newly created issues only with explicit justification.

## Open Questions

- The physical RFID hardware, reader protocol and identifier format remain a
  documented decision in issue #11; this does not block the QR MVP.
