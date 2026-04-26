# Implementation Plan: Mock Agent Runtime

## 1. Objective
Develop a "Mock Agent" utility that simulates Hermes/OpenClaw REST APIs and an SSH server.

## 2. Proposed Changes
- `scripts/mock_agent.py`: FastAPI app + AsyncSSH server.
- `docker/mock_agent.Dockerfile`: Dockerfile for the mock agent.
- `docker-compose.yml`: Add `mock-agent` service.
- `tests/integration/test_mock_agent_integration.py`: Integration tests.

## 3. Step-by-Step Execution Plan

### Step 1: Mock Agent Script
- **Task 1:** Implement a FastAPI app in `scripts/mock_agent.py` with:
    - `GET /status`: Returns online status, dummy tasks, dummy cron jobs.
    - `POST /chat`: Returns a echoed message or dummy response.
- **Task 2:** Add an SSH server to `scripts/mock_agent.py` using `asyncssh`. It should accept a specific username/password (e.g., `agent` / `agent_pass`) and allow basic commands like `tail`.

### Step 2: Containerization
- **Task 3:** Create `docker/mock_agent.Dockerfile`.
- **Task 4:** Add `mock-agent` to `docker-compose.yml`.

### Step 3: Verification
- **Task 5:** Write a test that adds this mock agent to the supervisor and checks status.

## 4. Verification Strategy
- **Manual Verification:** Build and run the mock agent container, then use the Dashboard (or curl) to verify it works.
- **Integration Test:** `pytest tests/integration/test_mock_agent_integration.py`.
