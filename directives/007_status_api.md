# Directive 007: Agent Status API

## Objective

Implement backend API proxying to fetch real-time agent tasks and operational status via the runtime adapters.

## Prerequisites

- [ ] Directive 004: Agent Registry API — Complete

## References

**PRD:**
- User Story: US-005 View Operational Status
- Functional Requirements: FR-6

**ARCH.md:**
- API Contracts: GET /api/agents/{id}/status
- Directory Structure: `backend/api/proxy.py`

## Scope

### In Scope
- Expand `AgentAdapter` to fully define and mock `get_status()`.
- Implement proxying logic that loads the agent from DB, invokes the adapter, and returns merged status.
- `GET /api/agents/{id}/status` endpoint.

### Out of Scope
- Frontend UI for status.

## Acceptance Criteria

- [ ] `GET /api/agents/{id}/status` retrieves agent details, forwards the call to the adapter, and returns JSON.
- [ ] Adapters return standard shapes (active tasks, cron jobs, overall state).
- [ ] Test suite mocks external API HTTP requests to verify proxy behavior.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes

## Status: [x] Complete

## Notes
