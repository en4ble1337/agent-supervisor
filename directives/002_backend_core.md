# Directive 002: Backend Core Setup (DB & Crypto)

## Objective

Initialize the FastAPI backend structure, set up the asynchronous SQLite database connection, and implement the encryption service for secure SSH credential storage.

## Prerequisites

- [x] Directive 001: Initial Environment Setup — Complete

## References

**PRD:**
- Functional Requirements: FR-1, FR-2
- Phase: Phase 1: Foundation & Discovery

**ARCH.md:**
- Data Models: Agent (prep for next directive)
- Directory Structure: `backend/core/config.py`, `backend/core/database.py`, `backend/services/crypto_service.py`

**RESEARCH.md:**
- Libraries: `cryptography` (`AESGCM` for AES-256-GCM credential encryption; legacy Fernet decrypt support is allowed only for old local records)

## Scope

### In Scope
- FastAPI application initialization.
- Asynchronous SQLAlchemy setup with SQLite (`aiosqlite`).
- Environment variable configuration loading (`ENCRYPTION_KEY`, `DATABASE_URL`).
- `CryptoService` implementation for encrypting/decrypting strings.

### Out of Scope
- Agent database models and REST API route handlers.

## Acceptance Criteria

- [ ] `CryptoService` successfully encrypts and decrypts a test string using `ENCRYPTION_KEY`.
- [ ] Database engine and sessionmaker are configured and successfully connect to the local SQLite file.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes
- [ ] Type checking and linting passes

## Implementation Notes

- Use Pydantic `BaseSettings` for configuration management in `config.py`.
- Ensure `ENCRYPTION_KEY` decodes to a 32-byte AES-256 key.
- New encrypted values must use the `v1:` AES-GCM token format. Legacy Fernet tokens may be readable during transition, but new writes must not use Fernet.

## Status: [x] Complete

## Notes

- 2026-05-03 audit: Updated to reflect the current AES-256-GCM implementation. The original Fernet wording conflicted with ARCH.md.
