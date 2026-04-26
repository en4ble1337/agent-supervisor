# Implementation Plan: Add Agent UI

## 1. Objective
Build the "Add Agent" form with robust client-side validation and specific error feedback for connection failures (`SSH_AUTH_FAILED`, `AGENT_UNREACHABLE`).

## 2. Proposed Changes
- `frontend/src/api.ts`: Add `createAgent` function.
- `frontend/src/pages/AddAgent.tsx`: Form component for adding an agent.
- `frontend/src/App.tsx`: Add basic routing between Dashboard and AddAgent (we can use simple state routing or `react-router-dom`). Since we need a "redirect", `react-router-dom` is best. I will install it.
- `frontend/src/tests/api.test.ts`: Add tests for `createAgent`.
- `frontend/src/tests/AddAgent.test.tsx`: Tests for form validation, submission, and error handling.

## 3. Step-by-Step Execution Plan

### Step 1: Dependencies and API
- **Task 1:** Install `react-router-dom`.
- **Task 2: [RED]** Write test for `api.ts` `createAgent`.
- **Task 3: [GREEN]** Implement `createAgent` in `api.ts` to post to `/api/agents`.

### Step 2: Add Agent Form (`AddAgent.tsx`)
- **Task 4: [RED]** Write test `AddAgent.test.tsx` verifying form inputs and validation errors (e.g., empty fields).
- **Task 5: [GREEN]** Implement basic form in `AddAgent.tsx` with controlled inputs.
- **Task 6: [RED]** Write test `AddAgent.test.tsx` verifying successful submission and navigation back to Dashboard.
- **Task 7: [GREEN]** Implement submission logic using `createAgent` and `useNavigate`.
- **Task 8: [RED]** Write test verifying specific error handling (e.g., `SSH_AUTH_FAILED` -> "Invalid SSH credentials", `AGENT_UNREACHABLE` -> "API unreachable").
- **Task 9: [GREEN]** Implement catch block inspecting the `error.response.data.error.code` to show the right UI message.

### Step 3: Routing (`App.tsx`)
- **Task 10: [REFACTOR]** Wrap `App` in `BrowserRouter` and configure routes `/` (Dashboard) and `/add` (AddAgent). Add "Add Agent" button to Dashboard.

## 4. Verification Strategy
- **Unit Tests:** `npm run test` using Vitest to test components.
- **Type Checking:** `npx tsc --noEmit`.

## 5. Potential Risks & Mitigations
- **Risk:** Handling Axios errors correctly in tests.
- **Mitigation:** Mock Axios errors matching the expected backend format (`{ response: { data: { error: { code: '...' } } } }`).
