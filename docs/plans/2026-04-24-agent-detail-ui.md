# Implementation Plan: Agent Operational UI

## 1. Objective
Build the `AgentDetail` page with tabbed navigation and the `OperationsTab` to display task lists and poll for status updates (`GET /api/agents/{id}/status`).

## 2. Proposed Changes
- `frontend/src/api.ts`: Add `getAgentStatus(id)` function.
- `frontend/src/pages/AgentDetail.tsx`: Main layout for agent details with tabs.
- `frontend/src/components/OperationsTab.tsx`: Component to display status, tasks, and cron jobs.
- `frontend/src/App.tsx`: Add route for `/agents/:id`.
- `frontend/src/components/AgentCard.tsx`: Make card clickable to navigate to detail page.
- `frontend/src/tests/AgentDetail.test.tsx`: Tests for tab navigation and polling.
- `frontend/src/tests/OperationsTab.test.tsx`: Tests for status display.

## 3. Step-by-Step Execution Plan

### Step 1: API and Navigation
- **Task 1: [RED]** Write test for `api.ts` `getAgentStatus`.
- **Task 2: [GREEN]** Implement `getAgentStatus` in `api.ts`.
- **Task 3: [REFACTOR]** Update `AgentCard.tsx` to wrap content in a `Link` to `/agents/:id`.

### Step 2: Agent Detail Shell (`AgentDetail.tsx`)
- **Task 4: [RED]** Write test `AgentDetail.test.tsx` verifying tab existence and active state.
- **Task 5: [GREEN]** Implement `AgentDetail.tsx` with a list of tabs (Operations, Chat, Files, Logs). Default to Operations.
- **Task 6: [REFACTOR]** Ensure responsive layout and dark-mode aesthetic.

### Step 3: Operations Tab (`OperationsTab.tsx`)
- **Task 7: [RED]** Write test `OperationsTab.test.tsx` verifying data rendering and refresh button.
- **Task 8: [GREEN]** Implement `OperationsTab.tsx`. Use `useEffect` with `setInterval` for 15-minute polling (for testing purposes, maybe allow configurable interval or just test the logic).
- **Task 9: [REFACTOR]** Ensure loading and error states are handled.

## 4. Verification Strategy
- **Unit Tests:** `npm run test` with Vitest.
- **Manual Verification:** (Via tests) Check polling interval logic.

## 5. Potential Risks & Mitigations
- **Risk:** 15-minute polling is too long to wait for in tests.
- **Mitigation:** Use `vi.useFakeTimers()` in Vitest to fast-forward time and verify polling triggers.
