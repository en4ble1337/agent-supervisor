# Implementation Plan: Multi-Agent Broadcast Messaging

## 1. Objective
Implement the capability to send a single message to multiple agents simultaneously (`POST /api/broadcast`) and build the `BroadcastConsole` UI component.

## 2. Proposed Changes
- `backend/services/broadcast_service.py`: Logic for parallel message delivery using `asyncio.gather`.
- `backend/api/broadcast.py`: Endpoint for broadcast messages.
- `backend/main.py`: Include `broadcast` router.
- `frontend/src/api.ts`: Add `sendBroadcast(content, businessGroup?, agentIds?)` function.
- `frontend/src/components/BroadcastConsole.tsx`: Component for sending and monitoring broadcasts.
- `frontend/src/pages/Dashboard.tsx`: Render `BroadcastConsole`.
- `tests/api/test_broadcast.py`: Tests for broadcast endpoint.
- `tests/services/test_broadcast_service.py`: Tests for parallel delivery.

## 3. Step-by-Step Execution Plan

### Step 1: Backend Broadcast Logic
- **Task 1: [RED]** Write test for `BroadcastService` verifying parallel execution.
- **Task 2: [GREEN]** Implement `BroadcastService` in `backend/services/broadcast_service.py`. It should take a list of agents and a message, use `AgentAdapter.send_message` in parallel, and record results (replies or errors).
- **Task 3: [RED]** Write test for `POST /api/broadcast`.
- **Task 4: [GREEN]** Implement `POST /api/broadcast` in `backend/api/broadcast.py`. Accept `content`, `business_group` (optional), and `agent_ids` (optional). Query DB for targeted agents, call `BroadcastService`.

### Step 2: Frontend Broadcast UI
- **Task 5: [RED]** Write test for `api.ts` `sendBroadcast`.
- **Task 6: [GREEN]** Implement `sendBroadcast` in `api.ts`.
- **Task 7: [RED]** Write test `BroadcastConsole.test.tsx` verifying form and result list.
- **Task 8: [GREEN]** Implement `BroadcastConsole.tsx`. Show individual results (Success/Failure/Reply) for each targeted agent.
- **Task 9: [REFACTOR]** Integrate `BroadcastConsole` into `Dashboard.tsx`.

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/api/test_broadcast.py tests/services/test_broadcast_service.py -v`.
- **Frontend Tests:** `npm run test` with Vitest.

## 5. Potential Risks & Mitigations
- **Risk:** Large number of agents causing timeouts or rate limiting on agent side.
- **Mitigation:** Use `asyncio.gather` with a semaphore if needed to limit concurrency, but for MVP, simple gather is fine.
- **Risk:** Storing broadcast results. 
- **Mitigation:** ARCH doesn't explicitly require persistent broadcast history in DB, just UI feedback. For MVP, we'll return the results in the response and display them.
