# Directive 014: Multi-Agent Broadcast Messaging

## Objective

Implement the capability to send a single message or command to multiple agents simultaneously, filtered by business group or explicit ID selection.

## Prerequisites

- [x] Directive 012: Messaging API — Complete
- [x] Directive 013: Frontend Chat Interface — Complete

## References

**PRD:**
- Phase 4: Advanced Operations (Extended)
- Note: PRD also lists multi-agent broadcasting as out of scope for MVP. This directive is therefore an extended/optional control-plane feature, not MVP readiness work.

**ARCH.md:**
- API Contracts: POST /api/broadcast
- Directory Structure: `backend/api/broadcast.py`, `backend/services/broadcast_service.py`, `frontend/src/components/BroadcastConsole.tsx`

## Scope

### In Scope
- `POST /api/broadcast` endpoint.
- `BroadcastService` for parallel execution of messages across agents.
- `BroadcastConsole` component in the Global Dashboard.
- Feedback mechanism to show which agents received the message and their individual replies.

### Out of Scope
- Scheduling broadcast messages for later.

## Acceptance Criteria

- [ ] User can select a Business Group and send a message to all agents in that group.
- [ ] UI displays a status list of replies as they come in from various agents.
- [ ] Backend handles partial failures (e.g., 3 agents succeed, 1 fails) without crashing.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes

## Status: [x] Complete

## Notes

- 2026-05-03 audit: This is intentionally outside the MVP scope. Before production use, add safety UX around target selection and operator confirmation so accidental cross-agent commands are harder to send.
