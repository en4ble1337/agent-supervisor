# Directive 023: Agent Connection Profile Hardening

## Objective

Make the Agent connection profile explicit enough for real heterogeneous runtimes instead of relying on hard-coded defaults.

## Prerequisites

- [x] Directive 004: Agent Registry API — Complete
- [x] Directive 009: SSH Files & Logs API — Complete
- [ ] Directive 020: Real Runtime Adapter Audit & Selection — Complete

## Scope

### In Scope
- Add model/schema/UI fields as needed for:
  - runtime type (`hermes`, `openclaw`, or future values)
  - SSH port
  - workspace path
  - default log path
  - optional API auth metadata if required by Directive 020
- Add Alembic migration for new persisted fields.
- Update Add Agent UI with runtime-aware defaults.
- Remove hard-coded `/opt/hermes/workspace` and `/var/log/syslog` assumptions from API routes.
- Preserve sensible defaults for the mock runtime and existing dev records.

### Out of Scope
- Secret rotation or key-based SSH auth, unless needed by the audited runtimes.

## Acceptance Criteria

- [ ] Agent model and migration include the agreed connection profile fields.
- [ ] Add Agent UI lets the operator choose runtime and override workspace/log defaults.
- [ ] SSH files and logs APIs use stored agent profile values.
- [ ] Existing tests cover default values and override values.
- [ ] `pytest tests/ -v`, `npm run test`, and `npm run build` pass.

## Status: [x] Incomplete / [ ] Complete
