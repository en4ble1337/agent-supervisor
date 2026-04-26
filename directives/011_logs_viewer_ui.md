# Directive 011: Frontend Logs Viewer

## Objective

Build the raw logs terminal view in the frontend to monitor agent output.

## Prerequisites

- [ ] Directive 008: Agent Operational UI — Complete
- [ ] Directive 009: SSH Files & Logs API — Complete

## References

**PRD:**
- User Story: US-005 View Operational Status (Logs tailing)

## Scope

### In Scope
- Logs tab within `AgentDetail.tsx`.
- Fetching raw text from `GET /api/agents/{id}/logs`.
- Displaying text in a scrollable, terminal-like dark background container.

### Out of Scope
- Real-time WebSocket streaming (polling is sufficient per MVP).

## Acceptance Criteria

- [ ] Logs tab fetches and displays raw log output formatting.
- [ ] "Refresh" button allows operator to pull the latest logs on demand.
- [ ] Container auto-scrolls to the bottom on load.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` passes

## Status: [x] Complete

## Notes
