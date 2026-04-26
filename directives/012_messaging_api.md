# Directive 012: Messaging API

## Objective

Implement the backend logic to send direct chat messages to agent runtimes and retrieve local history.

## Prerequisites

- [ ] Directive 004: Agent Registry API — Complete

## References

**PRD:**
- User Story: US-003 Direct 1-on-1 Chat with Agent
- Functional Requirements: FR-4

**ARCH.md:**
- API Contracts: POST /api/agents/{id}/chat
- Directory Structure: `backend/api/proxy.py`

## Scope

### In Scope
- Expand `AgentAdapter` with `send_message(text)`.
- `POST /api/agents/{id}/chat` endpoint proxying to the adapter.
- Local SQLite caching for session chat history (since runtimes may not support historical fetches).

### Out of Scope
- Multi-agent broadcast capabilities.

## Acceptance Criteria

- [ ] `POST /api/agents/{id}/chat` sends the message via the adapter and returns the agent's reply.
- [ ] Backend stores the chat thread temporarily in SQLite.
- [ ] Endpoint exists to fetch previous local session history for a specific agent.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes

## Status: [x] Complete

## Notes
