# Tasks

## 1. Baseline preservation

- [x] 1.1 Record the root file inventory, Git status, nested `Documentacion` repository status, frontend entry points, and current test inventory in the documentation migration map; verify every existing report and frontend asset has a recorded treatment.
- [x] 1.2 Run the existing backend test suite before structural work and record the command, result, and any network/model-dependent skips; verify `pytest` evidence is linked from the quality documentation.
- [x] 1.3 Compare `frontend/index.html` and `frontend/app/index.html` against the verification-station, administration, credential, and audit flows; verify the comparison identifies a proposed canonical entry point without deleting either copy.

## 2. Root orientation and collaboration

- [x] 2.1 Rewrite the root README around NotaryVerify's academic purpose, MVP, excluded real integrations, existing components, local entry points, and documentation links; verify every root link resolves locally.
- [x] 2.2 Create root `AGENTS.md` with the required reading order, architecture boundaries, privacy/data rules, branch and conventional-commit policy, OpenSpec flow, database-change protocol, test commands, and documentation update rules; verify it satisfies every requirement in `development-governance`.
- [x] 2.3 Extend `.gitignore` only for generated runtime, local environment, test-cache, model-cache, and editor artifacts that are actually produced; verify tracked source, safe fixtures, academic reports, and OpenSpec artifacts remain visible to Git.

## 3. Canonical documentation

- [x] 3.1 Perform the staged Windows-safe rename from `Documentacion` to canonical `documentacion` while retaining the nested repository and all historical files; verify the original report files and nested `.git` remain present after the rename.
- [x] 3.2 Create `documentacion/indice.md`, `academica/indice.md`, and the five `base/*/indice.md` files; verify navigation from the root index reaches every section and the historical-report mapping.
- [x] 3.3 Write the context documents for vision, problem/objectives, scope, academic limits, and explicitly deferred decisions; verify claims match the root README and do not present the prototype as legal identification.
- [x] 3.4 Write functional documentation for actors, high-priority requirements, non-functional requirements, use cases, and rules; verify every stated requirement is traceable to README/SRS source material or marked as pending.
- [x] 3.5 Write architecture documents for component communication, FastAPI boundaries, SQLite data model, API reference, runtime-data handling, and technical decisions; verify they describe the current code and identify non-implemented future decisions separately.
- [x] 3.6 Write roadmap, phases, backlog, and task-breakdown documents that distinguish current MVP work from later RFID, migration, and controlled-evaluation work; verify priorities and completion criteria are explicit.
- [x] 3.7 Write test strategy, security/privacy, deployment/local-operation, and conventions documents; verify they include the validation matrix, synthetic-data policy, and an evidence format for skipped checks.

## 4. Reproducible local operation

- [x] 4.1 Add a root `.env.example` containing only documented local ports and endpoint variables, plus comments that explain what is not yet environment-configurable; verify it contains no credentials, personal data, or biometric samples.
- [x] 4.2 Add the backend and static-frontend container definitions plus root `docker-compose.yml`, using the existing FastAPI and static client rather than a new framework or database service; verify `docker compose config` resolves successfully.
- [x] 4.3 Document native and Compose startup, shutdown, persistence, first-run model-download behavior, and endpoints in the README and operation guide; verify a clean checkout can follow the documented commands without inspecting source code.

## 5. Safe frontend consolidation

- [x] 5.1 Promote the verified canonical static frontend entry point to `frontend/` and preserve the alternate copy until parity validation passes; verify the canonical page retains verification, administration, credential, and audit flows.
- [x] 5.2 Update frontend README and root links to the canonical entry point and API configuration; verify the page opens through the documented static server and connects to the documented local API URL.
- [x] 5.3 Remove a superseded frontend copy only after the documented browser smoke check and a review of the baseline inventory; verify no required flow or referenced asset is lost, or retain the copy if parity cannot be demonstrated.

## 6. Validation and traceability

- [x] 6.1 Run a Markdown link and structure review across README, `AGENTS.md`, and `documentacion/`; verify there are no broken local links and all indexes are reachable from `documentacion/indice.md`.
- [x] 6.2 Run `pytest` for the backend and the documented API smoke checks after the bootstrap; verify results and justified skips are recorded in `documentacion/base/04-calidad-operacion/`.
- [x] 6.3 Build and start the Compose services, then verify the backend health endpoint, API documentation endpoint, and static frontend endpoint respond at their documented addresses.
- [x] 6.4 Execute the manual browser smoke checklist, including camera permission handling where hardware is available; verify any unavailable hardware or model-download check is recorded rather than silently treated as passing.
- [x] 6.5 Run `openspec validate bootstrap-profesional-notaryverify --strict` and review `openspec status --change bootstrap-profesional-notaryverify`; verify all artifacts validate and every completed task has supporting evidence before requesting review.
