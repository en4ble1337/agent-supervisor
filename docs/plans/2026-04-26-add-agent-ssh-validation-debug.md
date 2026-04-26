# Add Agent SSH Validation Debug Plan

### 1. Objective
Fix the Add Agent SSH validation path so a successful connection also proves a usable authenticated session by running a harmless remote command. Increase connection tolerance for slow network handshakes and add API-level logging for unexpected SSH validation exceptions.

### 2. Proposed Changes
- Modify `tests/services/test_ssh_service.py` to require `validate_connection()` to run `true` and pass a 10-second AsyncSSH connection timeout.
- Modify `tests/api/test_agents.py` to require `POST /api/agents` to log SSH validation exception details without logging the submitted password.
- Preserve the existing boolean service behavior by default, but let the API request exception propagation so route-level logs include the concrete AsyncSSH failure message.
- Modify `backend/services/ssh_service.py` to run `conn.run("true", check=True)` inside the connection context and set `connect_timeout=10`.
- Modify `backend/api/agents.py` to log unexpected SSH validation exceptions and return the existing `SSH_AUTH_FAILED` error shape.

### 3. Step-by-Step Execution Plan
- **Task 1: [RED] Write failing SSH service test**
  Confirm the existing service test fails because `validate_connection()` does not call `conn.run("true", check=True)` and does not pass `connect_timeout=10`.
- **Task 2: [RED] Write failing API logging test**
  Confirm `POST /api/agents` fails the test because `agents.py` does not currently catch and log exceptions from SSH validation.
- **Task 3: [GREEN] Implement minimal SSH validation change**
  Add `connect_timeout=10` to `asyncssh.connect()` in `validate_connection()` and execute `await conn.run("true", check=True)` before returning `True`.
- **Task 4: [GREEN] Implement minimal API logging change**
  Add a module logger in `backend/api/agents.py`, call SSH validation with exception propagation enabled, catch exceptions around SSH validation, log the target IP and exception message, then return the existing `SSH_AUTH_FAILED` response without including the SSH password.
- **Task 5: [REFACTOR] Clean up**
  Keep behavior narrow, avoid changing public API contracts, and ensure log messages remain useful but do not expose secrets.

### 4. Verification Strategy
- **Unit Tests:** Run `pytest tests/services/test_ssh_service.py tests/api/test_agents.py -v`.
- **Regression Tests:** Run `pytest tests/ -v` if targeted tests pass and the local environment can open the configured test database.
- **Manual Verification:** If Docker is available, rebuild/restart the backend and retry `POST /api/agents` against `10.1.20.191` with the provided SSH credentials, then inspect backend logs for the exact SSH validation message.

### 5. Potential Risks & Mitigations
- **Risk:** Running a remote command can fail even when auth succeeds if the account is restricted.
  **Mitigation:** Use `true`, which is harmless and only verifies command execution.
- **Risk:** Logging may accidentally expose the password.
  **Mitigation:** Log only IP address and exception text; never log request payloads or credentials.
- **Risk:** Increasing timeout conflicts with the architecture's 5-second non-functional target.
  **Mitigation:** This is a targeted Add Agent validation adjustment requested for observed network lag. Other SSH operations remain unchanged.
