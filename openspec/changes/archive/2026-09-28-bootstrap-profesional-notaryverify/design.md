# Design

## Context

See [proposal.md](proposal.md) for motivation and the two new capability
contracts. The current repository already implements the academic prototype:

- `backend/` is a FastAPI API with SQLAlchemy models, a runtime SQLite database,
  domain services, API routers and pytest tests. Its model groups are consent,
  simulated identities, credentials, users, verification sessions, audit events,
  verified documents and simulated procedures.
- `frontend/` is a dependency-free HTML/CSS/JavaScript interface. It currently
  contains both root files and a more complete `frontend/app/` station/admin
  interface, so a canonical entry point must be established without discarding
  either until parity is verified.
- `Documentacion/proyecto-si784-2026-ii-myprojectgroupcypw/` contains the
  academic reports and is itself a nested Git repository. On Windows,
  `Documentacion` and `documentacion` cannot coexist as distinct directories.
- `backend/data/` is ignored runtime state. The current `create_all` bootstrap
  is suitable for a disposable academic SQLite database but is not a migration
  mechanism.

The reference repository was used only to identify reusable practices: a concise
root README, a documentation index, scoped agent guidance, environment examples,
Docker Compose and explicit test/operation instructions. Its TypeScript/NestJS,
Next.js, Drizzle, OAuth and social-media domain are not applicable here.

## Goals / Non-Goals

**Goals:**

- Create one discoverable repository baseline without changing the NotaryVerify
  verification workflow or external institutional integrations.
- Retain the current FastAPI + SQLAlchemy + SQLite + pytest backend and the
  static JavaScript frontend; organize and document them proportionately.
- Make the academic scope, data-safety boundaries, run commands, architecture,
  roadmap and quality practices explicit.
- Provide a safe path to consolidate documentation and resolve duplicate
  frontend assets.

**Non-Goals:**

- Rebuild the frontend with React, Next.js or another framework.
- Replace SQLite, redesign the data model, introduce a production deployment,
  add authentication, or integrate Reniec/SID-Sunarp/signature services.
- Claim legal identity verification, use real citizen data, or add biometric
  datasets.
- Delete or rewrite academic reports during the bootstrap.

## Decisions

### 1. Keep the existing layered backend; document boundaries instead of refactoring

`backend/app/api` remains the HTTP boundary, `services` owns use-case and domain
logic, `models` owns SQLAlchemy/Pydantic representations, and `core` owns
cross-cutting configuration and persistence. `tests/` remains outside the
application package. The new architecture document will make these responsibilities
and API contracts explicit.

This fits the existing code and avoids a disruptive clean-architecture rewrite.
The alternative—adopting the reference project's NestJS module layout—would
replace working technology without helping the academic objective.

### 2. Use the existing static frontend as the intentional MVP client

The canonical frontend remains dependency-free HTML/CSS/JavaScript:

```text
frontend/
  index.html                 # canonical page after parity validation
  app.js                     # API calls and client interaction
  styles.css                 # styles for the canonical page
  README.md                  # local usage and API endpoint configuration
```

During application, the root page and `frontend/app/` must first be compared
against the current use cases (verification station, administration, credential
management and audit). The more complete verified interface becomes the canonical
entry point; the other copy is retained until the documented smoke check passes.
No framework or build tool is introduced because the current MVP needs camera
access and API interaction, not a component build pipeline.

### 3. Establish `documentacion/` as canonical with preservation-first migration

The target tree is:

```text
documentacion/
  indice.md
  base/
    00-contexto/             # vision, problem/objectives, scope
    01-funcional/            # actors, requirements, use cases, rules
    02-arquitectura/         # system, data, API, technical decisions
    03-planificacion/        # roadmap, phases, backlog, task breakdown
    04-calidad-operacion/    # tests, security, deployment, conventions
  academica/
    indice.md                # reports, original sources and their status
```

Every `base/*` section has an `indice.md`; new concise documentation summarizes
the current source of truth and links to the retained academic reports. Before a
case-only rename or any move, application inventories all files and records a
mapping. The nested repository remains intact as a recovery source until the
team explicitly approves its archival/removal after verification.

The alternative—maintaining `Documentacion/` separately—would preserve the
current split source of truth. Copying only selected reports without a mapping
would risk stale or lost academic material.

### 4. Provide reproducible development configuration without production claims

Root `.env.example` and `docker-compose.yml` describe local ports, the frontend
API base URL and named persistence for the existing backend runtime data. Compose
uses separate backend and static-frontend services; it does not provision a
database server because SQLite is the current approved store. Container images
and the documented native commands use a verified Python version compatible with
the backend dependencies.

The implementation must document that the current backend database URL is
code-derived and that this bootstrap does not silently change persistence
semantics. Moving it to a configurable `DATABASE_URL`, changing CORS policy, or
adding formal database migrations is deferred to an explicitly approved follow-up
because it affects compatibility and runtime behavior.

### 5. Put collaboration rules in one root `AGENTS.md`

`AGENTS.md` will contain the project objective, mandatory reading order,
architecture boundaries, safety and privacy rules, code/commit/branch conventions,
database-change protocol, test commands, OpenSpec workflow, and documentation
maintenance obligations. It will refer to detailed policies in `documentacion/`
rather than duplicate them. Scoped `AGENTS.md` files will be added only if a
subtree later requires instructions that differ materially from the root.

This gives people and AI agents a stable preflight with less drift than copying
generic instructions into every directory.

### 6. Define quality as layered evidence

The validation matrix will distinguish: static/documentation link checks,
`pytest` unit and integration tests, API smoke checks, manual browser/camera
smoke checks, and Docker Compose startup. A change records the applicable
evidence, plus a reason for any skipped hardware-, model-download-, or
network-dependent check. This preserves the current automated tests while making
the 80% coverage and 100 controlled biometric-attempt goals measurable future
quality work rather than claiming they are already achieved.

## Target repository layout

```text
/
  AGENTS.md
  README.md
  .env.example
  .gitignore
  docker-compose.yml
  backend/
    app/{api,core,models,services}/
    tests/
    requirements.txt
    README.md
    data/                     # generated; ignored
  frontend/
    index.html
    app.js
    styles.css
    README.md
  documentacion/
    indice.md
    base/{00-contexto,01-funcional,02-arquitectura,03-planificacion,04-calidad-operacion}/
    academica/
  openspec/
    specs/
    changes/
```

## Risks / Trade-offs

- [The nested `Documentacion` repository has independent history] → Inventory
  and retain it unchanged until the mapping, links and repository review pass.
- [Windows case-insensitivity complicates `Documentacion` → `documentacion`]
  → Use a staged, version-controlled rename and verify the result on Windows
  before removing any transitional location.
- [The two frontend copies may differ in behavior] → Make no deletion based on
  names; select the canonical page only after a documented use-case smoke check.
- [OpenCV/MediaPipe containers can have platform or model-download constraints]
  → Validate the backend image early, retain native startup instructions, and
  document any first-run network requirement.
- [SQLite `create_all` cannot evolve existing schemas safely] → Keep this
  bootstrap schema-neutral; make migration strategy a separate approved change.
- [Generic reference practices could pressure an unsuitable stack] → Retain
  practices only where they reduce ambiguity; do not adopt the reference code,
  framework or business logic.

## Migration Plan

1. Record the baseline file inventory, nested-repository status, existing
   frontend entry points and passing tests.
2. Add root guidance, environment examples, Docker Compose and canonical
   documentation indexes without moving existing material.
3. Create the documentation mapping and migrate or link retained reports using a
   reversible, staged rename; validate links on Windows.
4. Consolidate the frontend only after parity checks; retain a recovery path in
   the same branch until review is accepted.
5. Run the documented validation matrix and update the README/documentation with
   actual commands and outcomes.

Rollback consists of reverting the bootstrap commit(s); no runtime data,
academic report or nested Git history is deleted by this plan.

## Deferred Decisions

The bootstrap has no unresolved decision that blocks its task breakdown. The
following decisions are intentionally deferred to later product changes and
shall be recorded as pending in the canonical documentation:

- RFID hardware support versus a QR-only MVP demonstration.
- The synthetic consent and biometric-test record format for controlled
  evaluations.
- A future migration strategy when the SQLite schema must evolve beyond the
  current disposable local-database model.
