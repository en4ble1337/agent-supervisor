# Hermes Runtime Path Discovery Plan

## 1. Objective

Make the SSH-backed Files and Logs tabs useful against real Hermes installs that keep data under the SSH user's home directory instead of `/opt/hermes/workspace` and `/var/log/syslog`.

## 2. Proposed Changes

- `backend/services/ssh_service.py`
  - Add read-only discovery helpers for workspace root and log file path.
- `backend/api/ssh.py`
  - Resolve the workspace root per agent before applying traversal protection.
  - Use a discovered default log file when the operator does not provide `log_path`.
- `tests/services/test_ssh_service.py`
  - Cover workspace/log discovery parsing and command execution.
- `tests/api/test_ssh_api.py`
  - Cover dynamic workspace roots, traversal protection under dynamic roots, and discovered log defaults.

## 3. Step-by-Step Execution Plan

- **Task 1: [RED] Workspace root API tests**
  - Add tests proving `/api/agents/{id}/files` asks SSH for a workspace root and lists that root.
  - Add a traversal test proving `../etc` is still rejected before any SFTP read.
- **Task 2: [GREEN] Workspace root implementation**
  - Add `SSHService.resolve_workspace_root(...)`.
  - Update `resolve_workspace_path(...)` to accept the resolved root.
  - Update file listing and file content endpoints to use the resolved root.
- **Task 3: [RED] Log discovery tests**
  - Add a service test for discovered Hermes log paths.
  - Add an API test proving default `/logs` tails the discovered path.
- **Task 4: [GREEN] Log discovery implementation**
  - Add `SSHService.resolve_log_path(...)`.
  - Update `/logs` so only an omitted/default log path triggers discovery; explicit paths still tail exactly what the operator requests.
- **Task 5: [REFACTOR] Keep helpers small**
  - Ensure commands are read-only, bounded by the existing 5-second SSH timeout, and do not print secrets.
  - Keep traversal protection centralized and easy to audit.

## 4. Verification Strategy

- **Unit Tests**
  - `tests/services/test_ssh_service.py` covers command calls and fallback paths.
- **API Tests**
  - `tests/api/test_ssh_api.py` covers workspace root discovery, relative paths, traversal rejection, file content, and log discovery.
- **Manual Verification**
  - Call the local backend for the real agent:
    - `GET /api/agents/{id}/files`
    - `GET /api/agents/{id}/logs`
  - Confirm the response no longer fails on missing `/opt/hermes/workspace` or `/var/log/syslog`.

## 5. Potential Risks & Mitigations

- **Risk:** Discovery commands could accidentally leak environment secrets.
  - **Mitigation:** Only test file existence and print paths, never environment contents.
- **Risk:** Allowing dynamic roots could weaken traversal protection.
  - **Mitigation:** Resolve the root first, then normalize every requested path under that root and reject `..` segments.
- **Risk:** A missing workspace should still produce a clear error.
  - **Mitigation:** Return the legacy `/opt/hermes/workspace` fallback when no known directory exists, preserving existing behavior and error shape.
