# Directive 004: Agent Registry API

## Objective

Implement the database models and REST endpoints for registering, storing, and listing agents.

## Prerequisites

- [ ] Directive 003: SSH & Agent Adapter Foundation — Complete

## References

**PRD:**
- User Story: US-001 Add Agent via SSH, US-002 Filter Agents by Business Group
- Functional Requirements: FR-1, FR-2, FR-5

**ARCH.md:**
- Data Models: Agent
- API Contracts: POST /api/agents, GET /api/agents
- Directory Structure: `backend/models/agent.py`, `backend/schemas/agent_schemas.py`, `backend/api/agents.py`
- Error Codes: VALIDATION_ERROR, NOT_FOUND, AGENT_UNREACHABLE, SSH_AUTH_FAILED

## Scope

### In Scope
- SQLAlchemy `Agent` model.
- Pydantic schemas for creation and response.
- `POST /api/agents`: Validates SSH/API reachability, encrypts password, stores to DB.
- `GET /api/agents`: Lists agents, optionally filtered by `business_group`.

### Out of Scope
- Agent operational status endpoints (proxying).
- Frontend UI.

## Acceptance Criteria

- [ ] `POST /api/agents` rejects requests with invalid credentials via SSH/API validation logic.
- [ ] `POST /api/agents` stores the agent with an encrypted password using `CryptoService`.
- [ ] `GET /api/agents` returns the agent list WITHOUT the password field.
- [ ] `GET /api/agents?business_group=Acme` filters the list correctly.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes

## Implementation Notes

- Map internal validation failures from `SSHService` and `AgentAdapter` to `AGENT_UNREACHABLE` or `SSH_AUTH_FAILED` HTTP exceptions.

## Status: [x] Complete

## Notes
