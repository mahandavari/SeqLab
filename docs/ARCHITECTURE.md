# Architecture
## Product contract
A complete offline loop: import, explicit validation, real calculation, inspection, persistence and export. Single researcher on Windows. Original input is immutable. Only implemented workflows are exposed.

## Module dependency map
React components → typed JSON API → FastAPI routes → scientific functions / job runner → SQLAlchemy → SQLite.
Scientific functions use Biopython and defined linear-time statistics.
Charts use bundled Plotly. Future scientific engines will be separate adapters.

## Organization
frontend/src/components: import dialog, paginated sequence viewer, result views and charts.
frontend/src/lib: contracts, API client and presentation helpers.
backend/app/scientific: parsing, validation, transformation and calculations.
backend/app/database.py: relational schema.
backend/app/jobs.py: bounded background execution.
backend/app/main.py: API, exports and static frontend.
backend/tests, frontend/src tests and frontend/e2e: verification.

## Database schema, version 1
- projects: id, title, description, created_at.
- import_sources: id, project_id, original_text, created_at.
- sequences: id, project_id, identifier, description, sequence, kind, sha256, source_id, provenance, created_at.
- runs: id, project_id, sequence_id, input_hash, parameters, status, result, error, created_at, finished_at.

SQLite foreign keys and WAL are enabled. Imports are transactional. Duplicate identifiers reject a batch. Derived records reference their parent and its hash. Exported snapshots include schema_version=1.
Add explicit migrations before changing schema in a later release.

## Execution and constraints
Two worker threads, at most eight outstanding jobs. Startup fails interrupted runs. Cancellation suppresses late result writes, not hard CPU execution. No numerical cache; requested analyses recompute.
At this release's size limits, sequence text and results fit SQLite. Large datasets need a future filesystem storage/streaming layer.
The API rejects foreign browser origins and non-loopback hosts. No authentication is needed for the single-user localhost deployment; it must not be exposed as a shared server.

## Trade-offs
A static React build served by FastAPI is simpler to operate than a desktop sidecar during initial development. Tauri, signing, installer and upgrade support remain separate.
Custom CSS and local React state reduce initial dependencies. Large external engines are not emulated.
Current localization is English only; a localization layer and RTL testing are future work.
