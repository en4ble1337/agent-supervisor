# Directive 008: Agent Operational UI

## Objective

Build the Agent Detail shell and the Operations tab to display task lists and poll for status updates.

## Prerequisites

- [ ] Directive 006: Add Agent UI — Complete
- [ ] Directive 007: Agent Status API — Complete

## References

**PRD:**
- User Story: US-005 View Operational Status
- Functional Requirements: FR-6

**ARCH.md:**
- Directory Structure: `frontend/src/pages/AgentDetail.tsx`, `frontend/src/components/OperationsTab.tsx`

## Scope

### In Scope
- `AgentDetail` page with tabbed navigation structure (Operations, Chat, Files, Logs).
- Operations tab fetching from `GET /api/agents/{id}/status`.
- 15-minute polling mechanism and manual refresh button.
- Display layout for active tasks and cron jobs.

### Out of Scope
- Implementation of the Chat, Files, or Logs tabs.

## Acceptance Criteria

- [ ] Navigating to `/agents/:id` opens the detail view with the Operations tab active.
- [ ] Operations tab correctly displays status, tasks, and cron jobs fetched from backend.
- [ ] Manual refresh button triggers a fresh API call.
- [ ] Polling hook/logic executes every 15 minutes.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` passes

## Status: [x] Complete

## Notes
