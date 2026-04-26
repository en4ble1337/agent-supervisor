# Implementation Plan: Frontend Foundation & Global Dashboard

## 1. Objective
Set up the React application foundation (using Vite and TypeScript) with a dark-mode Tailwind CSS aesthetic. Implement the global dashboard view displaying the agent list with business group filtering.

## 2. Proposed Changes
- `frontend/`: Initialize Vite React+TS project.
- `frontend/src/services/api.ts`: API client setup for backend requests.
- `frontend/src/components/AgentCard.tsx`: Display component for individual agents.
- `frontend/src/pages/Dashboard.tsx`: Main view containing agent list and filter dropdown.
- `frontend/src/App.tsx`: Routing (if any) or main component rendering `Dashboard`.
- `frontend/src/tests/`: Vitest configuration and tests for `AgentCard` and `Dashboard`.

## 3. Step-by-Step Execution Plan

### Step 1: Scaffolding and Config
- **Task 1: [GREEN]** Run `npm create vite@latest frontend -- --template react-ts` (inside `run_shell_command`). Install Tailwind CSS, Vitest, React Testing Library, and Axios.
- **Task 2: [GREEN]** Configure `tailwind.config.js` for dark-mode terminal aesthetic (e.g. slate/zinc backgrounds, green/blue accents).
- **Task 3: [GREEN]** Configure `vite.config.ts` for Vitest and proxy `/api` requests to the backend (e.g., `http://localhost:8000`).

### Step 2: API Client (`api.ts`)
- **Task 4: [RED]** Write test for API client fetching agents. (Mock Axios).
- **Task 5: [GREEN]** Implement `api.ts` `getAgents(businessGroup?)` method.

### Step 3: Components
- **Task 6: [RED]** Write a test for `AgentCard.tsx` ensuring it renders agent name, ip, and business group.
- **Task 7: [GREEN]** Implement `AgentCard.tsx`.
- **Task 8: [RED]** Write a test for `Dashboard.tsx` ensuring it renders a list of `AgentCard`s and filters them based on a dropdown selection.
- **Task 9: [GREEN]** Implement `Dashboard.tsx` fetching data via `api.ts`.
- **Task 10: [REFACTOR]** Ensure types and styles align with technical aesthetic.

## 4. Verification Strategy
- **Unit Tests:** `npm run test` using Vitest to test components.
- **Type Checking:** `npx tsc --noEmit`.
- **Manual Verification:** (Skipped since we can't easily run the browser, but we rely on tests).

## 5. Potential Risks & Mitigations
- **Risk:** Vitest and RTL setup might be complex.
- **Mitigation:** Use standard configuration, install `@testing-library/react`, `@testing-library/jest-dom`, and `jsdom`.
