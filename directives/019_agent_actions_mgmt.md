# Directive 019: Agent Actions & Cron Management

## Objective

Extend the dashboard to not only view but also manage (create/delete) tasks and cron jobs on the agents.

## Prerequisites

- [ ] Directive 007: Agent Status API — Complete
- [ ] Directive 008: Agent Detail UI — Complete

## Scope

### In Scope
- `POST /api/agents/{id}/actions` to trigger specific agent tools or tasks.
- `POST /api/agents/{id}/crons` and `DELETE /api/agents/{id}/crons/{name}` for schedule management.
- UI elements in the "Operations" tab for these actions.

### Out of Scope
- Editing existing cron jobs (delete and recreate is sufficient for MVP).

## Acceptance Criteria

- [ ] Operator can successfully trigger a task on a remote agent via the UI.
- [ ] Operator can add a new scheduled job and see it appear in the cron list.
- [ ] All new code has corresponding tests in `tests/`

## Status: [x] Incomplete / [x] Complete
