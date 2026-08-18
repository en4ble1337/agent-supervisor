# Directive 018: Database Migrations (Alembic)

## Objective

Set up Alembic to manage database schema evolution for the SQLite agent registry.

## Prerequisites

- [x] Directive 002: Backend Core Setup — Complete

## References

**ARCH.md:**
- Tech Stack: SQLAlchemy 2.0+

## Scope

### In Scope
- Initialize Alembic in `backend/`.
- Configure `env.py` to support asynchronous `aiosqlite` migrations.
- Create the initial migration for the `Agent` model.

### Out of Scope
- Complex data migrations (schema only for now).

## Acceptance Criteria

- [ ] `alembic upgrade head` successfully creates the `agents` table.
- [ ] Initial migration includes every currently persisted model (`agents`, `chat_messages`, and any later connection-profile fields).
- [ ] Migration history is tracked and versioned.
- [ ] Documentation provided for creating new migrations.

## Status: [ ] Complete / [x] Migration Present / [ ] Runbook Verified

## Notes

- 2026-05-03 audit: The initial migration exists and includes `agents` and `chat_messages`, but there is no operator runbook proving when/how migrations are applied for local and Docker startup.
