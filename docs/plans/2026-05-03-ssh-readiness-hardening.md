# SSH Readiness Hardening

### 1. Objective
Make the SSH-backed parts of the supervisor safe enough for local testing and first real-agent trials. Fix the current gaps around SSH timeouts, workspace confinement, file content viewing, AES-256-GCM password encryption, and mock SSH/SFTP coverage.

### 2. Proposed Changes
- Update `tests/services/test_ssh_service.py` with failing tests for 5-second SSH timeouts, file reading, and SFTP path handling.
- Update `tests/api/test_ssh_api.py` with failing tests for workspace-relative file listing, traversal rejection, and file content responses.
- Update `tests/services/test_crypto_service.py` with failing assertions that encrypted SSH passwords use the AES-GCM token format.
- Update `tests/integration/test_mock_agent_integration.py` so at least one test exercises real mock SSH/SFTP behavior instead of patching SSH out.
- Update `backend/services/ssh_service.py` to apply strict 5-second timeouts to validation, SFTP listing, file reading, and log tailing.
- Update `backend/api/ssh.py` to confine file browsing to `/opt/hermes/workspace`, reject traversal, and expose a read-only file endpoint.
- Update `backend/services/crypto_service.py` to use AES-256-GCM with versioned tokens while optionally reading legacy Fernet tokens during transition.
- Update `frontend/src/api.ts` and `frontend/src/components/FileBrowser.tsx` to fetch and display text, markdown, and CSV files.
- Update `scripts/mock_agent.py` to support SFTP-backed directory listing and file reads for local integration testing.

### 3. Step-by-Step Execution Plan
- **Task 1: [RED] Write backend SSH timeout tests**
  Add tests that require `asyncssh.connect(..., connect_timeout=5)` and `conn.run(..., timeout=5)` for validation and logs.
- **Task 2: [RED] Write workspace confinement tests**
  Add API tests proving `/api/agents/{id}/files` resolves paths under `/opt/hermes/workspace` and rejects traversal like `../`.
- **Task 3: [RED] Write file-read tests**
  Add service and API tests for reading a file over SFTP and returning its path/content.
- **Task 4: [RED] Write AES-GCM tests**
  Update crypto tests so new encrypted values begin with a project token prefix and decrypt with AESGCM rather than Fernet.
- **Task 5: [RED] Write mock SSH/SFTP integration test**
  Add a test that starts the mock SSH server and verifies validation/list/read behavior without patching SSH.
- **Task 6: [GREEN] Implement minimal backend changes**
  Add timeout handling, safe path resolution, AES-GCM encryption, file read endpoint, and mock SFTP support.
- **Task 7: [GREEN] Implement minimal frontend changes**
  Replace the file-click alert with a viewer panel that loads and displays supported text content.
- **Task 8: [REFACTOR] Clean up and align docs/contracts**
  Keep names and response shapes clear, avoid leaking secrets in errors, and preserve compatibility where practical.

### 4. Verification Strategy
- **Unit Tests:** Run targeted backend tests for SSH, crypto, API SSH routes, and mock integration.
- **Backend Regression:** Run `python -m pytest tests/ -q` after dependencies are installed.
- **Frontend Tests:** Run `npm run test -- --run` and `npm run build` after `npm install`.
- **Manual Verification:** Use Docker Compose or local backend/frontend plus mock agent to add a mock agent, open Files, view a file, and open Logs.

### 5. Potential Risks & Mitigations
- **Existing encrypted values:** Fernet values already stored in a local DB will not match the new AES-GCM token format. The service will keep legacy decrypt support so existing test/dev rows can still be read.
- **Remote path differences:** Real agents may use a workspace other than `/opt/hermes/workspace`. For now, this hardens the documented default; a later directive should add a per-agent workspace field.
- **Mock SSH complexity:** AsyncSSH SFTP server support is more involved than command handling. Keep the mock filesystem tiny and deterministic so it remains useful for local tests.
