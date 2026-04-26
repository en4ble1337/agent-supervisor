# Implementation Plan: Frontend Logs Viewer

## 1. Objective
Build the raw logs terminal view in the frontend to monitor agent output (`GET /api/agents/{id}/logs`).

## 2. Proposed Changes
- `frontend/src/api.ts`: Add `getAgentLogs(id, logPath?)` function.
- `frontend/src/components/LogsViewer.tsx`: Component to display raw logs in a terminal-like container.
- `frontend/src/pages/AgentDetail.tsx`: Render `LogsViewer` in the Logs tab.
- `frontend/src/tests/LogsViewer.test.tsx`: Tests for log fetching and display.

## 3. Step-by-Step Execution Plan

### Step 1: API and Component
- **Task 1: [RED]** Write test for `api.ts` `getAgentLogs`.
- **Task 2: [GREEN]** Implement `getAgentLogs` in `api.ts`.
- **Task 3: [RED]** Write test `LogsViewer.test.tsx` verifying log fetching and rendering.
- **Task 4: [GREEN]** Implement `LogsViewer.tsx`. Use a pre-styled div with `overflow-y-auto` and `font-mono` to simulate a terminal.
- **Task 5: [REFACTOR]** Implement auto-scroll to bottom using `useRef` and `useEffect`.

### Step 2: Integration
- **Task 6: [REFACTOR]** Update `AgentDetail.tsx` to render `LogsViewer` in Logs tab.

## 4. Verification Strategy
- **Unit Tests:** `npm run test` with Vitest.
- **Type Checking:** `npx tsc --noEmit`.

## 5. Potential Risks & Mitigations
- **Risk:** Auto-scrolling might conflict with user manual scrolling.
- **Mitigation:** Only auto-scroll if the user is already near the bottom or on initial load. For MVP, simple scroll-to-bottom on load is sufficient.
