# Operator Cockpit Dashboard Refresh

## 1. Objective

Turn the global dashboard into a real operator cockpit instead of a simple agent card grid. The page should remove the multi-agent broadcast section, poll each visible Agent's status, and surface concrete operational statistics: total Agents, online/running Agents, Agents needing attention, active Tasks, Cron Jobs, Business Group distribution, and SSH/runtime intel availability.

## 2. Proposed Changes

- Modify `frontend/src/pages/Dashboard.tsx` to:
  - remove the `BroadcastConsole` import and rendered section;
  - fetch `getAgentStatus()` for every currently visible Agent after `getAgents()`;
  - render dashboard summary tiles, Business Group rollups, an Agent operations matrix, and active work/schedule panels;
  - preserve Business Group filtering and the Add Agent path.
- Modify `frontend/src/components/AgentCard.tsx` only if the card needs denser status-aware styling.
- Update `frontend/src/tests/Dashboard.test.tsx` to prove the new cockpit behavior and absence of broadcast UI.

## 3. Step-by-Step Execution Plan

- **Task 1: [RED] Write failing Dashboard tests**
  - Mock both `getAgents()` and `getAgentStatus()`.
  - Assert the dashboard polls status for visible Agents.
  - Assert summary statistics are rendered from real status payloads.
  - Assert the multi-agent broadcast section is absent.
- **Task 2: [GREEN] Implement status polling and summary model**
  - Add local status state keyed by Agent ID.
  - Use `Promise.allSettled()` so one unreachable Agent does not break the cockpit.
  - Compute counts for total Agents, online Agents, attention/unreachable Agents, active Tasks, and Cron Jobs.
- **Task 3: [GREEN] Replace the homepage layout**
  - Build a dense top bar with Business Group filter, refresh, and Add Agent.
  - Build compact metric tiles.
  - Build Business Group and Agent matrix sections inspired by Mission Control-style operational cards.
  - Build active Tasks/Cron Jobs/Runtime Intel panels.
- **Task 4: [REFACTOR] Tighten UI polish**
  - Keep cards shallow and avoid nested card layouts.
  - Use responsive grids with stable dimensions.
  - Keep copy terse and operator-focused.
- **Task 5: [VERIFY] Run frontend tests and build**
  - Run the focused Dashboard test first.
  - Run the full frontend test suite.
  - Run `npm run build`.
  - Reload the browser at `http://127.0.0.1:3001/`.

## 4. Verification Strategy

- **Unit Tests:** `npm run test -- Dashboard.test.tsx`
- **Full Frontend Tests:** `npm run test`
- **Build:** `npm run build`
- **Manual Verification:** Open `http://127.0.0.1:3001/`, confirm the dashboard shows operations metrics, the transcribo Agent appears, and no broadcast panel is visible.

## 5. Potential Risks & Mitigations

- **Slow status polling:** Use concurrent requests and `Promise.allSettled()` so one dead Agent degrades into an attention state instead of blocking the whole dashboard.
- **Status endpoint differences:** Treat missing task/cron arrays as empty and show runtime intel only when present.
- **UI overload:** Keep the top-level dashboard scan-friendly: summary tiles first, then groups, then Agent matrix and work queues.
