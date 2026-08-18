# Directive 020: Real Runtime Adapter Audit & Selection

## Objective

Replace assumed Hermes/OpenClaw endpoint behavior with verified runtime adapters based on the actual open-source products the supervisor is intended to sit on top of.

## Prerequisites

- [x] Directive 007: Agent Status API — Complete
- [x] Directive 012: Messaging API — Complete
- [x] Directive 019: Agent Actions & Cron Management — Code Complete

## References

**PRD:**
- Mission: Thin supervisor layer on top of OpenClaw and Hermes.
- Open Questions: Native API endpoints for Hermes and OpenClaw.

**ARCH.md:**
- Integration Points: OpenClaw API, Hermes API.
- Research: Multi-Runtime Adapter pattern.

## Scope

### In Scope
- Identify the actual OpenClaw and Hermes repositories, versions, API routes, request/response schemas, and auth requirements.
- Add a first-class `runtime` field to the Agent profile, or document why automatic detection is sufficient.
- Implement an adapter factory that selects `HermesAdapter` or `OpenClawAdapter` per agent instead of defaulting to Hermes everywhere.
- Update `get_status`, `send_message`, `trigger_action`, and cron methods to match real runtime contracts.
- Add tests using recorded or fixture-based runtime responses.

### Out of Scope
- Modifying upstream OpenClaw or Hermes.
- Adding new runtime families beyond OpenClaw and Hermes.

## Acceptance Criteria

- [ ] Documentation lists exact upstream repo/version/API references used for Hermes and OpenClaw.
- [ ] Each runtime adapter maps real upstream status, tasks, chat, action, and cron responses into the supervisor's internal shape.
- [ ] Agent records carry enough runtime metadata for correct adapter selection.
- [ ] Tests prove Hermes and OpenClaw adapters do not share placeholder endpoints unless upstream really does.
- [ ] Real-runtime API errors are mapped into the standard supervisor error shape.
- [ ] `pytest tests/ -v` passes.

## Status: [x] Incomplete / [ ] Complete

## Notes

- This is the highest-priority gap found in the 2026-05-03 directive audit.
