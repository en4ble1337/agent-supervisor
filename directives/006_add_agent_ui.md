# Directive 006: Add Agent UI

## Objective

Build the "Add Agent" form with robust client-side validation and specific error feedback for connection failures.

## Prerequisites

- [ ] Directive 005: Frontend Foundation & Global Dashboard — Complete

## References

**PRD:**
- User Story: US-001 Add Agent via SSH

**ARCH.md:**
- API Contracts: POST /api/agents
- Error Codes: AGENT_UNREACHABLE, SSH_AUTH_FAILED

## Scope

### In Scope
- Form to input IP, SSH credentials, API port, and Business Group.
- Client-side input validation.
- Integration with `POST /api/agents`.
- UI error states distinguishing between authentication failure and unreachable host.

### Out of Scope
- Modifying backend validation logic.

## Acceptance Criteria

- [ ] Form successfully posts to backend and adds the agent to the registry.
- [ ] UI clearly displays `SSH_AUTH_FAILED` or `AGENT_UNREACHABLE` based on backend error codes.
- [ ] Upon success, user is redirected back to the dashboard and the new agent appears.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` passes

## Status: [x] Complete

## Notes
