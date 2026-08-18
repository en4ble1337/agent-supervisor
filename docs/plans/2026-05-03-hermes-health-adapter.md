# Hermes Health Adapter Plan

## 1. Objective

Update the Hermes adapter so status checks work against the real Hermes API server endpoints observed on `10.1.20.201`: `/health` and `/v1/health`.

## 2. Proposed Changes

- `backend/services/agent_service.py`
  - Keep legacy `/status` support.
  - Fall back to Hermes `/health` and `/v1/health` for validation and status.
- `tests/services/test_agent_service.py`
  - Add tests for validation fallback.
  - Add tests for status fallback.

## 3. Step-by-Step Execution Plan

- **Task 1: [RED] Add adapter tests for health fallback**
  - Prove validation succeeds when `/status` is 404 but `/health` is 200.
  - Prove status returns a standard `AgentStatusResponse` shape when `/health` is 200.
- **Task 2: [GREEN] Implement health fallback**
  - Try `/status` first to preserve compatibility.
  - Try `/health`, then `/v1/health`.
  - Map health JSON to `status`, empty `active_tasks`, and empty `cron_jobs`.
- **Task 3: [REFACTOR] Keep OpenClaw behavior untouched**
  - Restrict this change to `HermesAdapter`.

## 4. Verification Strategy

- Run `python -m pytest tests/services/test_agent_service.py -q`.
- Run the full quality script.
- Call the local backend status endpoint for the real transcribo agent.

## 5. Potential Risks & Mitigations

- **Risk:** Health endpoints do not include task/cron detail.
  - **Mitigation:** Return the standard empty lists for now; richer Hermes capabilities need authenticated API-key support.
- **Risk:** Some older mock runtimes only expose `/status`.
  - **Mitigation:** Preserve `/status` as the first attempted endpoint.
