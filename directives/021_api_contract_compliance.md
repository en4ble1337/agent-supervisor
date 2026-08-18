# Directive 021: API Contract Compliance Pass

## Objective

Align backend/frontend request and response shapes with `docs/ARCH.md`, or explicitly update ARCH.md when the implemented contract is the better product choice.

## Prerequisites

- [x] Directive 004: Agent Registry API — Complete
- [x] Directive 012: Messaging API — Complete
- [x] Directive 014: Multi-Agent Broadcast Messaging — Complete
- [ ] Directive 020: Real Runtime Adapter Audit & Selection — Complete

## Scope

### In Scope
- Resolve `POST /api/agents/{id}/chat` contract drift: ARCH.md says request `{message}` and response `{reply}`, while implementation uses `{content}` and returns a stored `ChatMessage`.
- Resolve `POST /api/broadcast` contract drift: ARCH.md says `{message}`, while implementation uses `{content}`.
- Implement or explicitly remove the documented `409 Agent already exists` behavior for `POST /api/agents`.
- Ensure every backend error returns the standard `{ "error": { "code", "message", "details" } }` envelope.
- Update frontend API clients and tests after contract decisions.
- Add a concise API contract section to README or docs.

### Out of Scope
- Runtime-specific adapter internals, handled by Directive 020.

## Acceptance Criteria

- [ ] `docs/ARCH.md`, backend schemas, frontend API client, and tests agree on chat and broadcast payload names.
- [ ] Duplicate agent registration either returns `409` as documented or ARCH.md is updated to remove that promise.
- [ ] Error response tests cover 400, 401, 404, 409, and 502 paths.
- [ ] Frontend error handling displays the standardized error codes cleanly.
- [ ] `pytest tests/ -v`, `npm run test`, and `npx tsc --noEmit` pass.

## Status: [x] Incomplete / [ ] Complete
