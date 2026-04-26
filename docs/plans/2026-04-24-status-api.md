# Implementation Plan: Agent Status API

## 1. Objective
Implement backend API proxying to fetch real-time agent tasks and operational status via the runtime adapters (`GET /api/agents/{id}/status`).

## 2. Proposed Changes
- `backend/services/agent_service.py`: Expand `AgentAdapter`, `HermesAdapter`, and `OpenClawAdapter` to define a standard return shape for `get_status()`. For MVP, we can still return a mock but in a strictly defined Pydantic schema structure or Dict matching ARCH requirements (active tasks, cron jobs, overall state).
- `backend/schemas/agent_schemas.py`: Define `AgentStatusResponse` schema.
- `backend/api/proxy.py`: New router for `/api/agents/{id}/status`.
- `backend/main.py`: Include `proxy` router.
- `tests/api/test_proxy.py`: Tests for `GET /api/agents/{id}/status` mocking the adapter logic.
- `tests/services/test_agent_service.py`: Update adapter tests.

## 3. Step-by-Step Execution Plan

### Step 1: Adapter and Schema Update
- **Task 1: [RED]** Write test in `tests/services/test_agent_service.py` to assert adapters return a structured status dictionary.
- **Task 2: [GREEN]** Update `AgentAdapter`, `HermesAdapter`, and `OpenClawAdapter` in `backend/services/agent_service.py` to return the structured dictionary (`status`, `active_tasks`, `cron_jobs`).
- **Task 3: [REFACTOR]** Define `AgentStatusResponse` schema in `backend/schemas/agent_schemas.py`.

### Step 2: Proxy Endpoint
- **Task 4: [RED]** Create `tests/api/test_proxy.py` and write a failing test for `GET /api/agents/{id}/status`.
- **Task 5: [GREEN]** Create `backend/api/proxy.py`. Implement `GET /api/agents/{id}/status` endpoint. Fetch Agent from DB, get adapter (defaulting to Hermes for MVP), call `get_status()`, return combined response. 
- **Task 6: [REFACTOR]** Include router in `main.py`. Handle `404` if agent is not found.

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/api/test_proxy.py tests/services/test_agent_service.py -v`.
- **Type Checking:** Ensure correct return types.

## 5. Potential Risks & Mitigations
- **Risk:** Adapter `get_status` might block or fail if the external agent is down.
- **Mitigation:** Ensure the endpoint handles HTTP exceptions from the adapter gracefully, returning `502 Bad Gateway` or similar if the proxy fails. Since we are mocking the adapter response right now, this is less risky but the error handling structure should be in place.
