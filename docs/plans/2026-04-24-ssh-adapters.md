# Implementation Plan: SSH & Agent Adapter Foundation

## 1. Objective
Establish the base classes for agent communication (`AgentAdapter`, `HermesAdapter`, `OpenClawAdapter`) and implement the basic SSH verification logic (`SSHService`) required for validating new agent registrations.

## 2. Proposed Changes
- `backend/services/agent_service.py`: `AgentAdapter` abstract base class, `HermesAdapter`, and `OpenClawAdapter`.
- `backend/services/ssh_service.py`: `SSHService` with `validate_connection` method.
- `tests/services/test_agent_service.py`: Unit tests for adapter validation methods.
- `tests/services/test_ssh_service.py`: Unit tests for `SSHService.validate_connection`.

## 3. Step-by-Step Execution Plan

### Step 1: Agent Adapters (`agent_service.py`)
- **Task 1: [RED]** Write failing tests for `HermesAdapter.validate_endpoint()` and `OpenClawAdapter.validate_endpoint()` to return mock success/failure in `tests/services/test_agent_service.py`.
- **Task 2: [GREEN]** Implement `AgentAdapter` abstract class with abstract methods: `validate_endpoint`, `get_status`, `send_message`. Implement stubbed `HermesAdapter` and `OpenClawAdapter` returning mock responses in `backend/services/agent_service.py`.
- **Task 3: [REFACTOR]** Clean up type hints and imports.

### Step 2: SSH Verification (`ssh_service.py`)
- **Task 4: [RED]** Write a failing test for `SSHService.validate_connection()` using a mock for `asyncssh.connect` in `tests/services/test_ssh_service.py`. Test both successful connection and timeout (mocking `TimeoutError`).
- **Task 5: [GREEN]** Implement `SSHService.validate_connection(ip, user, password)` in `backend/services/ssh_service.py`. Use `asyncio.wait_for` or `asyncssh.connect(..., timeout=5)` to enforce a strict 5-second timeout.
- **Task 6: [REFACTOR]** Ensure exceptions from `asyncssh` are handled gracefully, returning a boolean or simple error enum.

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/services/test_agent_service.py tests/services/test_ssh_service.py -v`.
- **Manual Verification:** Tests pass, coverage for both success and failure (timeout, auth failure) paths.

## 5. Potential Risks & Mitigations
- **Risk:** SSH validation might block execution if timeout fails.
- **Mitigation:** Use native `asyncssh` timeout parameter and catch `asyncio.TimeoutError` and `OSError`.
