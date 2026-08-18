# SSH CLI Intel Bypass Plan

## 1. Objective

Use SSH to collect read-only runtime intelligence from Hermes when native API data is shallow or unavailable. The Operations tab should show what is happening under the agent, while avoiding broad remote-control UI.

## 2. Proposed Changes

- `backend/services/ssh_service.py`
  - Add a read-only `collect_runtime_intel(...)` helper that runs bounded Hermes CLI commands over SSH.
- `backend/api/proxy.py`
  - Enrich status responses with SSH CLI intel when SSH succeeds.
  - Keep API health/status as the top-level state, but include Hermes status, cron list, and sessions as observation data.
- `backend/schemas/agent_schemas.py`
  - Add an optional `intel` field to status responses.
- `frontend/src/api.ts`
  - Add TypeScript types for status intel sections.
- `frontend/src/components/OperationsTab.tsx`
  - Show a Runtime Intel panel.
  - Remove Quick Actions and Add/Delete Cron controls from the UI so this remains observability-first.
- Tests:
  - Backend service/API tests for CLI intel collection and status enrichment.
  - Frontend tests for rendering intel and preserving refresh behavior.

## 3. Step-by-Step Execution Plan

- **Task 1: [RED] Backend tests**
  - Add a service test for parsing Hermes CLI output into intel sections.
  - Add an API test proving successful status responses include SSH intel.
- **Task 2: [GREEN] Backend implementation**
  - Implement the read-only CLI collection command with marker-delimited sections.
  - Add status enrichment without making SSH intel failure fatal when the native API succeeds.
- **Task 3: [RED] Frontend tests**
  - Update OperationsTab tests to expect Runtime Intel content.
  - Add a test proving control forms are not rendered.
- **Task 4: [GREEN] Frontend implementation**
  - Render intel sections as compact preformatted panels.
  - Remove trigger/add/delete controls from the Operations tab.
- **Task 5: [REFACTOR] Verification**
  - Keep commands read-only and bounded by the existing SSH timeout.
  - Run focused tests, full quality checks, and a live smoke against the transcribo agent.

## 4. Verification Strategy

- `python -m pytest tests/services/test_ssh_service.py tests/api/test_proxy.py -q`
- `npm test -- OperationsTab.test.tsx --run`
- `.\scripts\check_quality.ps1`
- `npm run build`
- Live smoke: `GET /api/agents/e173d261-b8c0-4f45-ad21-fdd89e58cb58/status`

## 5. Potential Risks & Mitigations

- **Risk:** CLI commands accidentally mutate state.
  - **Mitigation:** Only call `status --all`, `cron list`, and `sessions list`.
- **Risk:** CLI output has terminal box drawing characters.
  - **Mitigation:** Treat output as text intel, not as fragile structured JSON.
- **Risk:** SSH intel slows status refresh.
  - **Mitigation:** Existing SSH command timeout remains 5 seconds, and frontend polling is only every 15 minutes.
