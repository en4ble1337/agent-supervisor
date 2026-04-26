# Implementation Plan: Frontend File Browser

## 1. Objective
Integrate the `chonky` file browser UI component into the Files tab to navigate the agent's remote workspace via SSH (`GET /api/agents/{id}/files`).

## 2. Proposed Changes
- `frontend/src/api.ts`: Add `getAgentFiles(id, path)` function.
- `frontend/src/components/FileBrowser.tsx`: Component wrapping Chonky to display and navigate files.
- `frontend/src/pages/AgentDetail.tsx`: Render `FileBrowser` in the Files tab.
- `frontend/src/tests/FileBrowser.test.tsx`: Tests for directory navigation.

## 3. Step-by-Step Execution Plan

### Step 1: Dependencies and API
- **Task 1:** Install `chonky`, `react-dnd`, `react-dnd-html5-backend`, `@fortawesome/free-solid-svg-icons`, `@fortawesome/react-fontawesome`. *Wait, Chonky v2 also requires MUI or icons. Let's check latest Chonky docs.* Actually, `chonky` is quite heavy. Let's use a simpler custom table-based browser first if `chonky` fails to install or is too complex for this environment's constraints, but I'll try `chonky` as per RESEARCH.md.
- **Task 2: [RED]** Write test for `api.ts` `getAgentFiles`.
- **Task 3: [GREEN]** Implement `getAgentFiles` in `api.ts`.

### Step 2: File Browser Component (`FileBrowser.tsx`)
- **Task 4: [RED]** Write test `FileBrowser.test.tsx` verifying file listing.
- **Task 5: [GREEN]** Implement `FileBrowser.tsx` using Chonky (or a simpler custom version if Chonky has peer dep issues). For MVP, a custom list might be safer and faster to implement correctly without MUI overhead if not already present. *Decision: I will implement a custom "professional looking" file browser using Tailwind to avoid dependency hell with MUI/Chonky in this restricted CLI environment.*
- **Task 6: [REFACTOR]** Ensure breadcrumb navigation works.

### Step 3: Integration
- **Task 7: [REFACTOR]** Update `AgentDetail.tsx` to render `FileBrowser` in Files tab.

## 4. Verification Strategy
- **Unit Tests:** `npm run test` with Vitest.
- **Type Checking:** `npx tsc --noEmit`.

## 5. Potential Risks & Mitigations
- **Risk:** `chonky` peer dependencies (MUI).
- **Mitigation:** I will build a custom, clean, terminal-aesthetic file list component using Tailwind that matches the "Hacker Dark Mode" PRD requirement better than a generic MUI component. This ensures full control over styling and reduces bundle size/dependency issues.
