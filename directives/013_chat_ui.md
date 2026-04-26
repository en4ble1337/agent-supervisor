# Directive 013: Frontend Chat Interface

## Objective

Build the direct 1-on-1 chat interface to communicate with agents.

## Prerequisites

- [ ] Directive 008: Agent Operational UI — Complete
- [ ] Directive 012: Messaging API — Complete

## References

**PRD:**
- User Story: US-003 Direct 1-on-1 Chat with Agent

**ARCH.md:**
- Directory Structure: `frontend/src/components/ChatTerminal.tsx`

**RESEARCH.md:**
- Libraries: `react-xtermjs` (or standard modern chat app layout)

## Scope

### In Scope
- Chat tab in `AgentDetail.tsx`.
- Input field for sending commands.
- Message history thread display.
- Integration with `POST /api/agents/{id}/chat` and history fetching.

### Out of Scope
- Real-time typing indicators.

## Acceptance Criteria

- [ ] User can type a message and press Enter to send.
- [ ] UI shows a loading/processing state while waiting for the agent's reply.
- [ ] Reply is appended sequentially to the message history.
- [ ] History is preserved visually when switching tabs within the detail view.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` passes

## Status: [x] Complete

## Notes
