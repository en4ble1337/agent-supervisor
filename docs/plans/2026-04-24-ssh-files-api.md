# Implementation Plan: SSH Files & Logs API

## 1. Objective
Implement SSH-based backend endpoints for listing workspace directories (`GET /api/agents/{id}/files`) and tailing log files (`GET /api/agents/{id}/logs`).

## 2. Proposed Changes
- `backend/services/ssh_service.py`: Add `list_directory(ip, user, pwd, path)` and `read_log_file(ip, user, pwd, log_path)` methods.
- `backend/api/ssh.py`: New router for `/api/agents/{id}/files` and `/api/agents/{id}/logs`.
- `backend/main.py`: Include `ssh` router.
- `tests/services/test_ssh_service.py`: Tests for directory listing and log tailing using mocks.
- `tests/api/test_ssh_api.py`: API tests for the new endpoints.

## 3. Step-by-Step Execution Plan

### Step 1: SSH Service Expansion
- **Task 1: [RED]** Write tests in `tests/services/test_ssh_service.py` for `list_directory` (mock SFTP readdir) and `read_log_file` (mock run command).
- **Task 2: [GREEN]** Implement `list_directory` using `asyncssh.start_sftp_client()`.
- **Task 3: [GREEN]** Implement `read_log_file` using `conn.run('tail -n 100 ...')`.
- **Task 4: [REFACTOR]** Ensure path validation to prevent directory traversal (e.g., check if path is relative or starts with restricted prefix if applicable, but for MVP we might just allow what SSH allows). Actually, acceptance criteria says "Input validation ensures `path` cannot execute malicious commands".

### Step 2: SSH API Router
- **Task 5: [RED]** Create `tests/api/test_ssh_api.py` and write failing tests for `GET /api/agents/{id}/files` and `GET /api/agents/{id}/logs`.
- **Task 6: [GREEN]** Create `backend/api/ssh.py`. Implement endpoints. Fetch Agent, decrypt password, call `SSHService`.
- **Task 7: [REFACTOR]** Include router in `main.py`. Handle exceptions and return standard error codes.

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/services/test_ssh_service.py tests/api/test_ssh_api.py -v`.
- **Integration Tests:** Use mocks for `asyncssh` to verify command generation and response parsing.

## 5. Potential Risks & Mitigations
- **Risk:** Command injection in `path` parameter.
- **Mitigation:** Use `shlex.quote` or ensure `path` is passed as an argument to `tail` correctly. For SFTP `readdir`, it's generally safer as it's an API call, not a shell command.
- **Risk:** Large log files.
- **Mitigation:** `tail -n 100` limits output size.
